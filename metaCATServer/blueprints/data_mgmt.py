# -*- coding:utf-8 -*-
##############################################
#  DATA MANAGEMENT Blueprint
##############################################
import os
from flask import jsonify, request, session, send_file, render_template, Blueprint
from flask_babel import gettext

import shutil
from utils.mongo_util import db
from utils import authenticate
from utils import comm_util
from comm_config import __DEFAULT_PATH, TERM_ANNOTATING, TERM_PARAPHRASING, \
    TBL_METADATA, TBL_BATCHSTATUS, TBL_ANNOTATING, TBL_PARAPHRASING, \
    DATA_VERSION, CURRENT_VERSION

data_mgmt_bp = Blueprint('data_mgmt', __name__)


@data_mgmt_bp.route('/user_list', methods=['GET'])
def handle_user_list():
    """
    取得注册用户列表
    :return:
    """
    user_list = authenticate.registered_user_list()
    return jsonify(user_list)


@data_mgmt_bp.route('/batch_allocation_page', methods=['GET'])
def handle_batch_allocation_page():
    """管理员批次分配"""
    return render_template('batchAllocation.html')


@data_mgmt_bp.route('/metadata', methods=['GET'])
def handle_metadata():
    metadatas = db[TBL_METADATA].find()
    metadata_list = []
    for metadata in metadatas:
        metadata_list.append({
            "category": metadata["category"],
            "metadata_name": metadata["metadata_name"]
        })
    return jsonify(metadata_list)


@data_mgmt_bp.route('/metadata/<category>/<metadata_name>', methods=['GET'])
def handle_metadata_detail(category, metadata_name):
    metadata = db[TBL_METADATA].find_one({'category': category, 'metadata_name': metadata_name})
    return jsonify(metadata['metadata_value'])


@data_mgmt_bp.route('/batch_allocation_list', methods=['GET'])
def handle_batch_allocation_list():
    """
    取得未分配批次列表
    :return:
    """
    batch_category = request.args.get('batch_category')
    unallocate_path = __DEFAULT_PATH + '/unallocated/' + batch_category
    batch_list = []
    index = 0
    for parent, dirs, files in os.walk(unallocate_path, followlinks=True):
        files.sort()
        for name in files:
            index += 1
            batch_list.append({
                "index": index,
                "batch_id": name.replace('.json', ''),
                "metadata_name": os.path.split(parent)[-1]
            })

    return jsonify(batch_list)


@data_mgmt_bp.route('/batch_allocation', methods=['POST'])
def handle_batch_allocation():
    """
    批次分配
    :return:
    """
    data = request.get_json()

    batch_category = data['batch_category']
    batch_id_list = data['batch_id_list']
    allocate_login_name = data['allocate_login_name']

    unallocate_path = __DEFAULT_PATH + '/unallocated/' + batch_category

    error_key = comm_util.get_time_keyword()
    error_time = comm_util.get_time_stamp()
    error_path = __DEFAULT_PATH + '/error/DUP' + error_key
    comm_util.create_dirs(error_path)

    error_docs = []
    error_docsfile = error_path + '.json'
    error_zipfile = error_path + '.zip'

    batch_status = db[TBL_BATCHSTATUS].find_one({'login_name': allocate_login_name})
    if batch_status == None:
        batch_status = comm_util.generate_default_batchstatus(allocate_login_name)

    for batch in batch_id_list:
        batch_id = batch['batch_id']
        metadata_name = batch['metadata_name']
        srcfile = os.path.join(unallocate_path, metadata_name, batch_id + '.json')
        duplicatefile = os.path.join(error_path, batch_id + '.json')

        # batch_info = db[TBL_BATCHSTATUS].find_one(
        #     {'login_name': allocate_login_name, batch_category: {"batch_id": batch_id}})
        dup_query = {'login_name': allocate_login_name, batch_category: {
            '$elemMatch': {
                'batch_id': batch_id
            }
        }}
        # print(dup_query)
        batch_info = db[TBL_BATCHSTATUS].find_one(dup_query)

        # 如果同批次文件已经分配给该用户，作为重复文件记录
        if batch_info:
            print('{} already exists'.format(batch_id))
            shutil.move(srcfile, duplicatefile)  # 移动文件到重复文件夹
            error_docs.append({
                "batch_id": batch_id,
                "batch_category": batch_category,
                "batch_file": batch_id + '.json',
                "exception": 'batch file duplicated'
            })
        else:
            batch_status[batch_category].append({"batch_id": batch_id,
                                                 "batch_progress": "0%",
                                                 "metadata_name": metadata_name,
                                                 "batch_description": "Initialized"})
            dialogue_name = "dialogue_" + batch_category
            dialogues = comm_util.load_json_file(srcfile)
            for key, value in dialogues.items():
                # value["active"] = False
                # print("srcfile:=", srcfile, "key:=", key, "value:=", value)
                value["dialogue_id"] = key
                value["activated"] = False
                value["status"] = "PROCESSING"
                # 增加激活状态，便于第一次数据保存
                db[dialogue_name].save(
                    {'login_name': allocate_login_name, "batch_id": batch_id, "metadata_name": metadata_name,
                     DATA_VERSION: CURRENT_VERSION,
                     "dialogue": value})

            os.remove(srcfile)  # 删除文件

    # 保存batch列表处理状态
    db[TBL_BATCHSTATUS].save(batch_status)

    if len(error_docs) > 0:
        # 保存错误日志
        error_info = {
            "error_type": "ALLOCATION",
            "operator": allocate_login_name,
            "error_docs": error_docs,
            "error_time": error_time
        }
        comm_util.save_json_file(error_info, error_docsfile)
        # 压缩错误文件
        comm_util.compress_folder(error_zipfile, error_path)

        responseObject = {
            "code": 100,
            "msg": gettext(u'msgErrorAllocateBatch')
        }
    else:
        responseObject = {
            "code": 200,
            "msg": gettext(u'msgSuccessAllocateBatch')
        }

    # 删除错误收集文件夹
    comm_util.rm_folder_tree(error_path)

    return jsonify(responseObject)
