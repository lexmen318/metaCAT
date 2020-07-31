# -*- coding:utf-8 -*-
##############################################
#  SYSTEM ADMIN Blueprint
##############################################
import random, os
from flask import jsonify, session, request, abort, Blueprint
from flask_babel import gettext
from utils.mongo_util import db
from utils import comm_util
# from bson.son import SON
from comm_config import __DEFAULT_PATH, TBL_MEMBERS, TBL_BATCHSTATUS, TBL_ANNOTATING, TBL_PARAPHRASING, \
    DATA_VERSION, CURRENT_VERSION, TERM_ANNOTATING, TERM_PARAPHRASING
from paraphrasing.paraphrasing_convertor import convert_real_slot_value

sys_admin_bp = Blueprint('sys_admin', __name__)


@sys_admin_bp.route("/session")
def handle_session():
    """获取session的数据"""
    index = random.randint(1, 100)
    name_value = "python" + str(index)
    session["name"] = name_value
    session["mobile"] = "18612345678"
    return "session saved as " + name_value


@sys_admin_bp.route("/sessionShow")
def handle_session_show():
    """获取session的数据"""
    name = session.get("name")
    mobile = session.get("mobile")
    return "return hello %s-%s" % (name, mobile)


@sys_admin_bp.route('/data_convert_operations')
def handle_data_convert_operations():
    operations = {
        "convertOperation": [
            {
                "title": gettext(u'funcUpdateDataVersion'),
                "url": "/sys_admin/update_current_version"
            },
            {
                "title": gettext(u'funcConsistencyCheck'),
                "url": "/sys_admin/consistency_check"
            },
            {
                "title": gettext(u'funcUpdateParaphrasingRealValue'),
                "url": "/sys_admin/update_paraphrasing_real_value"
            }
            # , {
            #     "title": "示例更新1",
            #     "url": "/sys_admin/data_convert_from_v0_to_v1"
            # }, {
            #     "title": "示例更新2",
            #     "url": "/sys_admin/data_convert_from_v1_to_v2"
            # }
        ],
        "clearOperation": [
            {
                "title": gettext(u'funcRemoveAnnotating'),
                "url": "/sys_admin/remove_annotating"
            },
            {
                "title": gettext(u'funcRemoveParaphrasing'),
                "url": "/sys_admin/remove_paraphrasing"
            }
        ],
    }

    return jsonify(operations)


@sys_admin_bp.route('/update_current_version')
def handle_update_current_version():
    """
    更新数据版本
    :return:
    """
    general_query = {DATA_VERSION: {'$ne': CURRENT_VERSION}}
    user_list = db[TBL_MEMBERS].find(general_query)
    for item in user_list:
        item[DATA_VERSION] = CURRENT_VERSION
        db[TBL_MEMBERS].save(item)

    batch_status_list = db[TBL_BATCHSTATUS].find(general_query)
    for item in batch_status_list:
        item[DATA_VERSION] = CURRENT_VERSION
        db[TBL_BATCHSTATUS].save(item)

    annotating_list = db[TBL_ANNOTATING].find(general_query)
    for item in annotating_list:
        item[DATA_VERSION] = CURRENT_VERSION
        db[TBL_ANNOTATING].save(item)

    paraphrasing_status_list = db[TBL_PARAPHRASING].find(general_query)
    for item in paraphrasing_status_list:
        item[DATA_VERSION] = CURRENT_VERSION
        db[TBL_PARAPHRASING].save(item)

    responseObject = {"status": "success"}
    return jsonify(responseObject)


@sys_admin_bp.route('/consistency_check')
def handle_consistency_check():
    """
    数据完整性检测
    :return:
    """

    error_key = comm_util.get_time_keyword()
    error_time = comm_util.get_time_stamp()
    error_path = __DEFAULT_PATH + '/error/CHK' + error_key
    comm_util.create_dirs(error_path)

    error_docs = []

    error_docsfile = error_path + '.json'
    error_zipfile = error_path + '.zip'

    general_query = {}
    batch_status_list = db[TBL_BATCHSTATUS].find(general_query)
    for batch_item in batch_status_list:
        login_name = batch_item['login_name']

        # 检查annotating列表完整性
        annotating_list = batch_item[TERM_ANNOTATING]
        for annotating_item in annotating_list:
            batch_id = annotating_item['batch_id']
            dialogue_list = db[TBL_ANNOTATING].find({'login_name': login_name, "batch_id": batch_id})
            if dialogue_list.count() == 0:
                error_docs.append('annotating列表与Status列表比匹配')

        # 检查paraphrasing列表完整性
        paraphrasing_list = batch_item[TERM_PARAPHRASING]
        for paraphrasing_item in paraphrasing_list:
            batch_id = paraphrasing_item['batch_id']
            dialogue_list = db[TBL_PARAPHRASING].find({'login_name': login_name, "batch_id": batch_id})
            if dialogue_list.count() == 0:
                error_docs.append('paraphrasing列表与Status列表比匹配')

    # annotating聚合检查
    # {"$sort": SON([("count", -1), ("_id", -1)])}
    pipeline = [
        # {"$match": {DATA_VERSION: CURRENT_VERSION}},
        {"$group": {"_id": {'login_name': '$login_name', 'batch_id': '$batch_id'}, "count": {"$sum": 1}}}
    ]
    annotating_aggregate = db[TBL_ANNOTATING].aggregate(pipeline)
    for annotating_item in annotating_aggregate:
        condition = annotating_item['_id']
        login_name = condition['login_name']
        batch_id = condition['batch_id']
        existing_query = {'login_name': login_name, 'annotating': {
            '$elemMatch': {
                'batch_id': batch_id
            }
        }}
        batch_info = db[TBL_BATCHSTATUS].find_one(existing_query)
        if batch_info == None:
            error_docs.append('annotating的dialogue在Status列表中不存在，login_name:={}， batch_id:={}'
                              .format(login_name, batch_id))

    paraphrasing_aggregate = db[TBL_PARAPHRASING].aggregate(pipeline)
    for paraphrasing_item in paraphrasing_aggregate:
        condition = paraphrasing_item['_id']
        login_name = condition['login_name']
        batch_id = condition['batch_id']
        existing_query = {'login_name': login_name, 'paraphrasing': {
            '$elemMatch': {
                'batch_id': batch_id
            }
        }}
        batch_info = db[TBL_BATCHSTATUS].find_one(existing_query)
        if batch_info == None:
            error_docs.append('paraphrasing的dialogue在Status列表中不存在，login_name:={}， batch_id:={}'
                              .format(login_name, batch_id))

    if len(error_docs) > 0:
        # 保存错误日志
        error_info = {
            "error_type": "CHECK",
            "operator": "Administrator",
            "error_docs": error_docs,
            "error_time": error_time
        }
        comm_util.save_json_cn_file(error_info, error_docsfile)

        error_file = os.path.join(error_path, 'error.log')
        comm_util.save_txt_file(error_docs, error_file)
        # 压缩错误文件
        comm_util.compress_folder(error_zipfile, error_path)
        # 删除错误文件夹
        comm_util.rm_folder_tree(error_path)

    responseObject = {"status": "success"}
    return jsonify(responseObject)


@sys_admin_bp.route('/data_convert_from_v0_to_v1')
def handle_data_convert_from_v0_to_v1():
    responseObject = {"status": "success"}
    return jsonify(responseObject)


@sys_admin_bp.route('/data_convert_from_v1_to_v2')
def handle_data_convert_from_v1_to_v2():
    responseObject = {"status": "success"}
    return jsonify(responseObject)


@sys_admin_bp.route('/remove_annotating')
def handle_remove_annotating():
    """
    清除annotating数据
    :return:
    """
    db[TBL_ANNOTATING].delete_many({})
    batch_status_list = db[TBL_BATCHSTATUS].find({})
    for item in batch_status_list:
        item[DATA_VERSION] = CURRENT_VERSION
        item["annotating"] = []
        db[TBL_BATCHSTATUS].save(item)

    responseObject = {"status": "success"}
    return jsonify(responseObject)


@sys_admin_bp.route('/remove_paraphrasing')
def handle_remove_paraphrasing():
    """
    清除paraphrasing数据
    :return:
    """
    db[TBL_PARAPHRASING].delete_many({})
    batch_status_list = db[TBL_BATCHSTATUS].find({})
    for item in batch_status_list:
        item[DATA_VERSION] = CURRENT_VERSION
        item["paraphrasing"] = []
        db[TBL_BATCHSTATUS].save(item)

    responseObject = {"status": "success"}
    return jsonify(responseObject)


@sys_admin_bp.route('/update_paraphrasing_real_value')
def handle_update_paraphrasing_real_value():
    paraphrasing_item_list = db[TBL_PARAPHRASING].find({})
    for item in paraphrasing_item_list:
        # if item['dialogue']['dialogue_id'] in ['TWHR0100', 'FHA0150', 'HN0100', 'RN0100']:
        #     print('here!')
        convert_real_slot_value(item)
        db[TBL_PARAPHRASING].save(item)

    responseObject = {"status": "success"}
    return jsonify(responseObject)
