# -*- coding:utf-8 -*-
##############################################
#  SYSTEM MANAGEMENT Blueprint
##############################################
import os
from flask import jsonify, request, session, send_file, render_template, Blueprint
from werkzeug.utils import secure_filename
from flask_babel import gettext
import shutil
from utils.mongo_util import db
from utils import authenticate
from utils import comm_util, sysInit_util
from annotating.data_convertor import DataConvertor
from annotating.annotating_loader import DataLoader
from comm_config import __DEFAULT_PATH, TERM_ANNOTATING, TERM_PARAPHRASING, \
    TBL_METADATA, TBL_BATCHSTATUS, TBL_ANNOTATING, TBL_PARAPHRASING, \
    DATA_VERSION, CURRENT_VERSION

sys_mgmt_bp = Blueprint('sys_mgmt', __name__)


@sys_mgmt_bp.route('/sys_init', methods=['GET'])
def handle_sys_init():
    """
    系统初始化
    :return:
    """
    raw_path = __DEFAULT_PATH + '/raw'
    comm_util.create_dirs(raw_path)

    # 创建annotating分配目录
    unallocate_annotating_path = __DEFAULT_PATH + '/unallocated/annotating'
    comm_util.create_dirs(unallocate_annotating_path)
    metadata_annotating_list = db[TBL_METADATA].find({'category': 'annotating'})
    for metadata in metadata_annotating_list:
        metadata_name = metadata["metadata_name"]
        unallocate_annotating_path = __DEFAULT_PATH + '/unallocated/annotating/' + metadata_name
        comm_util.create_dirs(unallocate_annotating_path)

    # 创建paraphrasing分配目录
    unallocate_paraphrasing_path = __DEFAULT_PATH + '/unallocated/paraphrasing'
    comm_util.create_dirs(unallocate_paraphrasing_path)
    metadata_paraphrasing_list = db[TBL_METADATA].find({'category': 'paraphrasing'})
    for metadata in metadata_paraphrasing_list:
        metadata_name = metadata["metadata_name"]
        unallocate_annotating_path = __DEFAULT_PATH + '/unallocated/paraphrasing/' + metadata_name
        comm_util.create_dirs(unallocate_annotating_path)

    export_path = __DEFAULT_PATH + '/export'
    comm_util.create_dirs(export_path)

    error_path = __DEFAULT_PATH + '/error'
    comm_util.create_dirs(error_path)

    user_list = authenticate.registered_user_list()
    for user in user_list:
        login_name = user['login_name']
        batch_status = db[TBL_BATCHSTATUS].find_one({'login_name': login_name})
        if batch_status == None:
            # 创建新的batch状态列表
            default_batch_status = comm_util.generate_default_batchstatus(login_name)
            db[TBL_BATCHSTATUS].save(default_batch_status)

    # 系统设置初始化
    sysInit_util.sys_setting_init()

    responseObject = {
        "code": 200,
        "msg": gettext(u'msgInitDataSuccess')
    }
    return jsonify(responseObject)


@sys_mgmt_bp.route('/error_file_list', methods=['GET'])
def handle_error_file_list():
    """
    返回错误列表
    :return:
    """
    error_path = __DEFAULT_PATH + '/error'
    comm_util.create_dirs(error_path)

    error_list = []
    index = 0
    files = os.listdir(error_path)
    for file in files:
        # 获取目录或者文件的路径
        dir_file_path = os.path.join(error_path, file)
        # 判断该路径为文件还是路径
        if os.path.isfile(dir_file_path) and file.endswith('.json'):
            index += 1
            error_key = file.replace('.json', '')
            error_json = comm_util.load_json_file(dir_file_path)
            error_type = error_json['error_type']
            operator = error_json['operator']
            error_time = error_json['error_time']
            error_list.append({
                "index": index,
                "error_key": error_key,
                "error_type": error_type,
                "operator": operator,
                "error_time": error_time,
                "json_url": "/sys_mgmt/download_error_file/" + error_key + "/json",
                "zip_url": "/sys_mgmt/download_error_file/" + error_key + "/zip"
            })

    return jsonify(error_list)


@sys_mgmt_bp.route('/remove_error/<error_key>', methods=['GET'])
def handle_remove_error(error_key):
    """
    删除异常文件
    :param error_key:
    :return:
    """

    error_path = __DEFAULT_PATH + '/error'
    error_json_filename = error_path + '/' + error_key + '.json'
    error_zip_filename = error_path + '/' + error_key + '.zip'

    comm_util.rm_file(error_json_filename)
    comm_util.rm_file(error_zip_filename)

    responseObject = {
        "code": 200,
        "msg": gettext(u'msgErrorFileDeleted')
    }

    return jsonify(responseObject)


@sys_mgmt_bp.route('/download_error_file/<error_key>/<suffix>', methods=['GET'])
def handle_download_error_file(error_key, suffix):
    """
    下载异常文件
    :param error_key:
    :param suffix:
    :return:
    """
    error_filename = __DEFAULT_PATH + '/error/' + error_key + '.' + suffix
    return send_file(error_filename, as_attachment=True)


@sys_mgmt_bp.route('/upload_metadata', methods=['POST'])
def handle_upload_metadata():
    """
    元数据导入
    :return:
    """
    raw_path = __DEFAULT_PATH + '/raw'
    f = request.files['metadata_file']
    # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
    upload_file_name = os.path.join(raw_path, secure_filename(f.filename))
    f.save(upload_file_name)

    metadata_json = comm_util.load_json_file(upload_file_name)
    metadata = db[TBL_METADATA].find_one(
        {'category': metadata_json['category'], 'metadata_name': metadata_json['metadata_name']})
    if metadata:
        responseObject = {
            "code": 100,
            "msg": gettext(u'msgMetadataExisting')
        }
    else:
        # 增加激活状态，便于第一次数据保存
        db[TBL_METADATA].save({'category': metadata_json['category'], 'metadata_name': metadata_json['metadata_name'],
                               DATA_VERSION: CURRENT_VERSION, 'metadata_value': metadata_json['metadata_value']})

        responseObject = {
            "code": 200,
            "msg": gettext(u'msgMetadataUploaded')
        }

    return jsonify(responseObject)


@sys_mgmt_bp.route('/upload_batch_allocation/<content_category>', methods=['POST'])
def handle_upload_batch_allocation(content_category):
    """
    上传批次文件
    :return:
    """
    # Create unallocated file path
    raw_unzip_path = __DEFAULT_PATH + '/raw/' + comm_util.get_time_keyword()
    comm_util.create_dirs(raw_unzip_path)

    raw_path = __DEFAULT_PATH + '/raw'
    unallocate_path = __DEFAULT_PATH + '/unallocated'

    error_key = comm_util.get_time_keyword()
    error_time = comm_util.get_time_stamp()
    error_path = __DEFAULT_PATH + '/error/UPD' + error_key
    comm_util.create_dirs(error_path)

    f = request.files['batch_file']
    # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
    upload_file_name = os.path.join(raw_path, secure_filename(f.filename))
    f.save(upload_file_name)

    # 解压缩上传文件
    comm_util.uncompress_file(upload_file_name, raw_unzip_path)

    manifest_file = raw_unzip_path + '/MANIFEST.json'
    if not os.path.exists(manifest_file):
        responseObject = {
            "code": 100,
            "msg": gettext(u'msgMANIFESTNotExists')
        }
        return jsonify(responseObject)

    manifest = comm_util.load_json_file(manifest_file)
    if "Batch-category" not in manifest:
        responseObject = {
            "code": 100,
            "msg": gettext(u'msgBatchCategoryNotDefined')
        }
        return jsonify(responseObject)

    if "metadata_name" not in manifest:
        responseObject = {
            "code": 100,
            "msg": gettext(u'msgMetadataNameNotDefined')
        }
        return jsonify(responseObject)

    batch_category = manifest["Batch-category"]
    metadata_name = manifest["metadata_name"]

    if metadata_name == 'NA':
        # 当metadata_name为NA是不检测元数据的存在
        pass
    else:
        metadata = db[TBL_METADATA].find_one({'category': batch_category, 'metadata_name': metadata_name})
        if metadata == None:
            responseObject = {
                "code": 100,
                "msg": gettext(u'msgMetadataNotExisting:[{0}][{1}]').format(batch_category, metadata_name)
            }
            return jsonify(responseObject)

    error_docs = []
    error_docsfile = error_path + '.json'
    error_zipfile = error_path + '.zip'
    for root, dirs, files in os.walk(raw_unzip_path):
        for raw_filename in files:
            if raw_filename == 'MANIFEST.json':
                continue

            # raw_file = raw_unzip_path + '/' + raw_filename
            raw_file = os.path.join(root, raw_filename)

            # 创建目标分配路径
            target_path = unallocate_path + '/' + batch_category + '/' + metadata_name
            comm_util.create_dirs(target_path)

            target_file = unallocate_path + '/' + batch_category + '/' + metadata_name + '/' + raw_filename
            error_file = os.path.join(error_path, raw_filename)
            try:
                if batch_category == TERM_ANNOTATING:
                    if content_category == 'JSON':
                        raw_dialogueDict = comm_util.load_json_file(raw_file)
                        target_dialogueDict = DataConvertor.from_dataset(raw_dialogueDict, data_set=metadata_name)
                        comm_util.save_json_file(target_dialogueDict, target_file)
                    elif content_category == 'RAW':
                        target_dialogueDict = DataLoader.load_raw_data(raw_file)
                        comm_util.save_json_file(target_dialogueDict, target_file)
                else:
                    if content_category == 'JSON':
                        # shutil.move(raw_file, target_file)  # 移动文件到未分配文件夹
                        # 读取JSON之后保存，避免不合法的JSON文件混入
                        raw_dialogueDict = comm_util.load_json_file(raw_file)
                        comm_util.save_json_file(raw_dialogueDict, target_file)
                    elif content_category == 'RAW':
                        pass

            except Exception as e:
                print('Json transfer fails, INFO: %s' % str(e))
                error_docs.append({
                    "batch_id": raw_filename.replace('.json', ''),
                    "batch_file": raw_filename,
                    "exception": str(e),
                })
                shutil.copy(raw_file, error_file)  # 复制文件

    # 删除解压缩原始文件夹
    comm_util.rm_folder_tree(raw_unzip_path)

    if len(error_docs) > 0:
        # 保存错误日志
        error_info = {
            "error_type": "UPLOAD",
            "operator": "Administrator",
            "error_docs": error_docs,
            "error_time": error_time
        }
        comm_util.save_json_file(error_info, error_docsfile)
        # 压缩错误文件
        comm_util.compress_folder(error_zipfile, error_path)

        responseObject = {
            "code": 100,
            "msg": gettext(u'msgErrorUploadBatch'),
            "error_docsfile": error_docsfile,
            "error_docs": error_docs
        }
    else:

        responseObject = {
            "code": 200,
            "msg": gettext(u'msgSuccessUploadBatch')
        }

    # 删除错误文件夹
    comm_util.rm_folder_tree(error_path)

    return jsonify(responseObject)


@sys_mgmt_bp.route('/annotating_export_origin', methods=['GET'])
def handle_annotating_export_origin():
    """
    导出annotating数据
    :return:
    """
    export_key = comm_util.get_time_keyword()
    export_path = __DEFAULT_PATH + '/export/' + export_key
    export_batch_path = __DEFAULT_PATH + '/export/' + export_key + '/batch'
    export_zipfile = export_path + '.zip'
    comm_util.create_dirs(export_batch_path)

    all_batch_status_file = export_path + '/all_batch_status.json'
    all_batch_status = []

    batch_status_list = db[TBL_BATCHSTATUS].find()
    for status_item in batch_status_list:
        user_name = status_item["login_name"]

        # 导出用户的Batch列表
        for batch_item in status_item[TERM_ANNOTATING]:
            batch_id = batch_item["batch_id"]
            all_batch_status.append({
                "login_name": user_name,
                "batch_id": batch_id,
                "batch_progress": batch_item['batch_progress'],
                "batch_description": batch_item['batch_description']
            })

            dialogue_list = db[TBL_ANNOTATING].find({'login_name': user_name, "batch_id": batch_id})
            user_dialogues = {}
            for dialogue_item in dialogue_list:
                dialogue = dialogue_item["dialogue"]
                user_dialogues[dialogue["dialogue_id"]] = dialogue

            # 导出用户的Batch文件
            dstfile = os.path.join(export_batch_path, batch_id + ".json")
            # comm_util.save_json_file(user_dialogues, dstfile)
            comm_util.save_json_cn_file(user_dialogues, dstfile)

    # 导出全部batchStatus文件
    # comm_util.save_json_file(all_batch_status, all_batch_status_file)
    comm_util.save_json_cn_file(all_batch_status, all_batch_status_file)

    # 压缩导出文件
    comm_util.compress_folder(export_zipfile, export_path)

    # 删除导出文件夹
    comm_util.rm_folder_tree(export_path)

    '''下载压缩文件'''
    return send_file(export_zipfile, as_attachment=True)


@sys_mgmt_bp.route('/annotating_export_multiwox', methods=['GET'])
def handle_annotating_export_multiwox():
    """
    导出annotating multiwox数据
    :return:
    """
    export_key = comm_util.get_time_keyword()
    export_path = __DEFAULT_PATH + '/export/' + export_key
    export_batch_path = __DEFAULT_PATH + '/export/' + export_key + '/batch'
    export_zipfile = export_path + '.zip'
    comm_util.create_dirs(export_batch_path)

    error_docs = []
    error_path = __DEFAULT_PATH + '/error/EXP' + export_key
    comm_util.create_dirs(error_path)

    error_docsfile = error_path + '.json'
    error_zipfile = error_path + '.zip'

    all_batch_status_file = export_path + '/all_batch_status.json'
    all_batch_status = []

    batch_status_list = db[TBL_BATCHSTATUS].find()
    for status_item in batch_status_list:
        user_name = status_item["login_name"]

        # 导出用户的Batch列表
        for batch_item in status_item[TERM_ANNOTATING]:
            batch_id = batch_item["batch_id"]
            all_batch_status.append({
                "login_name": user_name,
                "batch_id": batch_id,
                "batch_progress": batch_item['batch_progress'],
                "batch_description": batch_item['batch_description']
            })

            dialogue_list = db[TBL_ANNOTATING].find({'login_name': user_name, "batch_id": batch_id})
            user_dialogues = {}
            for dialogue_item in dialogue_list:
                dialogue = dialogue_item["dialogue"]
                user_dialogues[dialogue["dialogue_id"]] = dialogue

            # 导出用户的Batch文件
            dstfile = os.path.join(export_batch_path, batch_id + ".json")
            error_file = os.path.join(error_path, batch_id + ".json")
            try:
                target_dialogueDict = DataConvertor.to_dataset(user_dialogues, data_set='MultiWOZ')
                # comm_util.save_json_file(target_dialogueDict, dstfile)
                comm_util.save_json_cn_file(target_dialogueDict, dstfile)
            except Exception as e:
                print('Json transfer fails, INFO: %s' % str(e))
                error_docs.append({
                    "batch_id": batch_id,
                    "batch_file": batch_id + ".json",
                    "exception": str(e),
                })
                # 普通格式导出
                # comm_util.save_json_file(user_dialogues, error_file)
                comm_util.save_json_cn_file(user_dialogues, error_file)

    # 导出全部batchStatus文件
    # comm_util.save_json_file(all_batch_status, all_batch_status_file)
    comm_util.save_json_cn_file(all_batch_status, all_batch_status_file)

    # 压缩导出文件
    comm_util.compress_folder(export_zipfile, export_path)

    # 删除导出文件夹
    comm_util.rm_folder_tree(export_path)

    if len(error_docs) > 0:
        error_time = comm_util.get_time_stamp()
        # 保存错误日志
        error_info = {
            "error_type": "EXPORT",
            "operator": "Administrator",
            "error_docs": error_docs,
            "error_time": error_time
        }
        # comm_util.save_json_file(error_info, error_docsfile)
        comm_util.save_json_cn_file(error_info, error_docsfile)
        # 压缩错误文件
        comm_util.compress_folder(error_zipfile, error_path)

        # 删除错误原始文件夹
        comm_util.rm_folder_tree(error_path)

    '''下载压缩文件'''
    return send_file(export_zipfile, as_attachment=True)


@sys_mgmt_bp.route('/paraphrasing_export_origin', methods=['GET'])
def handle_paraphrasing_export_origin():
    """
    导出paraphrasing数据
    :return:
    """
    export_key = comm_util.get_time_keyword()
    export_path = __DEFAULT_PATH + '/export/' + export_key
    export_batch_path = __DEFAULT_PATH + '/export/' + export_key + '/batch'
    export_zipfile = export_path + '.zip'
    comm_util.create_dirs(export_batch_path)

    all_batch_status_file = export_path + '/all_batch_status.json'
    all_batch_status = []

    batch_status_list = db[TBL_BATCHSTATUS].find()
    for status_item in batch_status_list:
        user_name = status_item["login_name"]

        # 导出用户的Batch列表
        for batch_item in status_item[TERM_PARAPHRASING]:
            batch_id = batch_item["batch_id"]
            all_batch_status.append({
                "login_name": user_name,
                "batch_id": batch_id,
                "batch_progress": batch_item['batch_progress'],
                "batch_description": batch_item['batch_description']
            })

            dialogue_list = db[TBL_PARAPHRASING].find({'login_name': user_name, "batch_id": batch_id})
            user_dialogues = {}
            for dialogue_item in dialogue_list:
                dialogue = dialogue_item["dialogue"]
                user_dialogues[dialogue["dialogue_id"]] = dialogue

            # 导出用户的Batch文件
            dstfile = os.path.join(export_batch_path, batch_id + ".json")
            # comm_util.save_json_file(user_dialogues, dstfile)
            comm_util.save_json_cn_file(user_dialogues, dstfile)

    # 导出全部batchStatus文件
    # comm_util.save_json_file(all_batch_status, all_batch_status_file)
    comm_util.save_json_cn_file(all_batch_status, all_batch_status_file)

    # 压缩导出文件
    comm_util.compress_folder(export_zipfile, export_path)

    # 删除导出文件夹
    comm_util.rm_folder_tree(export_path)

    '''下载压缩文件'''
    return send_file(export_zipfile, as_attachment=True)
