# -*- coding:utf-8 -*-
##############################################
#  SYSTEM ADMIN Blueprint
##############################################
from comm_config import TBL_METADATA, TBL_BATCHSTATUS, TBL_ANNOTATING, DATA_VERSION, CURRENT_VERSION, TERM_ANNOTATING

from flask import jsonify, session, request, abort, Blueprint
from utils.mongo_util import db
from utils import comm_util, cache_util
from annotating import annotating_validator, annotating_loader

# == Local ==
from annotating.data_convertor import DataConvertor

annotating_bp = Blueprint('annotating', __name__)


@annotating_bp.route("/dialogues_metadata/<batch_id>", methods=['GET'])
def handle_dialogues_metadata(batch_id):
    """
    GET - All dialogues metadata

    PUT - Handle
    """

    login_name = comm_util.get_session_login_name()
    dialogue_list = db[TBL_ANNOTATING].find({'login_name': login_name, "batch_id": batch_id}) \
        .sort("dialogue.dialogue_id")
    responseObject = []
    for item in dialogue_list:
        dialogueObject = item["dialogue"]
        dialogueID = dialogueObject['dialogue_id']
        dialogueTurnList = dialogueObject['turns']
        responseObject.append(
            {"id": dialogueID, "num_turns": len(dialogueTurnList), "status": dialogueObject['status']})
    return jsonify(responseObject)


@annotating_bp.route("/dialogues_metadata/<dialog_id>", methods=['PUT'])
def handle_dialogues_metadata_put(dialog_id):
    data = request.get_json()

    id = data["id"]

    login_name = comm_util.get_session_login_name()
    dialogue = db[TBL_ANNOTATING].find_one({"login_name": login_name, 'dialogue.dialogue_id': dialog_id})
    # 保存新的对话ID
    dialogue["dialogue"]["dialogue_id"] = id
    db[TBL_ANNOTATING].save(dialogue)

    # 删除旧的对话
    db[TBL_ANNOTATING].delete_one({'login_name': login_name, "dialogue.dialogue_id": dialog_id})
    responseObject = {"status": "success"}

    return jsonify(responseObject)


@annotating_bp.route("/dialogues_main/<batch_id>", methods=["GET", "POST"])
def handle_dialogues_main(batch_id):
    """
    GET - All dialogues

    POST - Create a new one, either from data(json, string) or empty
    """
    login_name = comm_util.get_session_login_name()
    responseObject = {}

    if request.method == "GET":
        dialogues = db[TBL_ANNOTATING].find({"login_name": login_name, "batch_id": batch_id})
        for item in dialogues:
            dialogue = item["dialogue"]
            responseObject[dialogue["dialogue_id"]] = dialogue

        if id == 'MultiWOZ':
            responseObject = DataConvertor.to_dataset(responseObject, data_set=id)

    if request.method == "POST":
        # 新建对话时，数据为空
        data = request.get_json()
        # 根据既有的Dialog得到metadata_name
        existing_dialogue = db[TBL_ANNOTATING].find_one({"login_name": login_name, "batch_id": batch_id})
        if existing_dialogue:
            metadata_name = existing_dialogue["metadata_name"]
        else:
            metadata_name = 'MULTIWOZ'

        new_dialogue_id = 'Dialogue_NEW' + comm_util.get_timestamp_key()
        dialogue = {
            "dialogue_id": new_dialogue_id,
            "activated": False,
            "status": "PROCESSING",
            "turns": []
        }

        new_dialogue = {
            "login_name": login_name, "batch_id": batch_id,
            "batch_id": batch_id,
            "metadata_name": metadata_name,
            "data_version": CURRENT_VERSION,
            "dialogue": dialogue
        }
        db[TBL_ANNOTATING].save(new_dialogue)
        responseObject = {"id": new_dialogue_id}

    return jsonify(responseObject)


@annotating_bp.route("/dialogues_detail/<batch_id>/<dialogue_id>", methods=["GET", "POST", "PUT", "DELETE"])
def handle_dialogues_detail(batch_id, dialogue_id):
    """
    GET - All dialogues

    PUT - change specific dialogue with a dialogue
    """
    login_name = comm_util.get_session_login_name()
    dialogue = db[TBL_ANNOTATING].find_one(
        {"login_name": login_name, "batch_id": batch_id, 'dialogue.dialogue_id': dialogue_id})

    if not dialogue:
        responseObject = {"status": "failure",
                          "msg": "对话未找到, batch_id:=%s, dialogue_id:=%s" % (str(batch_id), str(dialogue_id))}
        return jsonify(responseObject)

    if 'metadata_name' not in dialogue.keys():
        responseObject = {"status": "failure",
                          "msg": "MetadataName缺失, batch_id:=%s, dialogue_id:=%s" % (str(batch_id), str(dialogue_id))}
        return jsonify(responseObject)

    # 生成Metadata缓存key, 放入缓存
    metadata_name = dialogue['metadata_name']
    metadata_value = get_current_metadata_value(metadata_name)

    if request.method == "GET":
        item = dialogue["dialogue"]
        responseObject = {"dialogue": item["turns"], "metadata_name": metadata_name, "metadata": metadata_value}

    if request.method == "PUT":
        turn_list = request.get_json()

        for turn in turn_list:
            usr_validation, sys_validation = annotating_validator.validate_turn(turn, metadata_value)

            # 保存检测结果
            turn['usr']['turn_info'] = usr_validation
            turn['sys']['turn_info'] = sys_validation

        # 删除旧的Dialogue
        db[TBL_ANNOTATING].delete_one(
            {'login_name': login_name, "batch_id": batch_id, "dialogue.dialogue_id": dialogue_id})

        # 保存新的Dialogue
        new_dialogue = {'login_name': login_name, "batch_id": batch_id,
                        "metadata_name": metadata_name,
                        DATA_VERSION: CURRENT_VERSION,
                        "dialogue": {"dialogue_id": dialogue_id, "activated": True, "status": "PROCESSING",
                                     "turns": turn_list}}
        db[TBL_ANNOTATING].save(new_dialogue)
        responseObject = {"status": "success"}

    if request.method == "DELETE":
        db[TBL_ANNOTATING].delete_one(
            {'login_name': login_name, "batch_id": batch_id, "dialogue.dialogue_id": dialogue_id})
        responseObject = {"status": "success"}

    return jsonify(responseObject)


def get_current_metadata_value(metadata_name):
    medatadata_key = cache_util.generate_medatadata_key(TERM_ANNOTATING, metadata_name)
    metadata_value = cache_util.get(medatadata_key)
    if metadata_value == None:
        # 缓存刷新后，要重新取得
        metadata = db[TBL_METADATA].find_one(
            {'category': TERM_ANNOTATING, 'metadata_name': metadata_name})
        metadata_value = metadata['metadata_value']
        cache_util.put(medatadata_key, metadata_value)

    return metadata_value


@annotating_bp.route("/validate_turn/<batch_id>/<dialogue_id>/<turn_id>", methods=["PUT"])
def handle_annotating_validate_turn(batch_id, dialogue_id, turn_id):
    """
    校验一个对话轮次
    :param batch_id:
    :param dialogue_id:
    :param turn_id:
    :return:
    """

    data = request.get_json()
    metadata_name = data['metadata_name']
    turn = data['turn']

    # login_name = comm_util.get_session_login_name()
    # dialogue = db[TBL_ANNOTATING].find_one(
    #     {"login_name": login_name, "batch_id": batch_id, 'dialogue.dialogue_id': dialogue_id})
    # metadata_name = dialogue['metadata_name']
    metadata_value = get_current_metadata_value(metadata_name)

    usr_validation, sys_validation = annotating_validator.validate_turn(turn, metadata_value)
    validate_result = {
        "usr": usr_validation,
        "sys": sys_validation
    }
    return jsonify(validate_result)


@annotating_bp.route("/validate_dialogues/<batch_id>/<dialogue_id>", methods=["PUT"])
def handle_annotating_validate_dialogues(batch_id, dialogue_id):
    """
    校验对话轮次
    :param batch_id:
    :param dialogue_id:
    :return:
    """

    data = request.get_json()
    metadata_name = data['metadata_name']
    turn_list = data['turn_list']

    # login_name = comm_util.get_session_login_name()
    # dialogue = db[TBL_ANNOTATING].find_one(
    #     {"login_name": login_name, "batch_id": batch_id, 'dialogue.dialogue_id': dialogue_id})
    # metadata_name = dialogue['metadata_name']
    metadata_value = get_current_metadata_value(metadata_name)
    validate_result = annotating_validator.validate_dialogue(turn_list, metadata_value)
    # validate_result = {'status': 'success'}
    return jsonify(validate_result)


@annotating_bp.route("/dialogue_status", methods=["POST"])
def handle_dialogue_status():
    # st = time.time()
    data = request.get_json()
    batch_id = data['batch_id']
    dialogue_id = data['dialogue_id']
    currentStatus = data['currentStatus']

    login_name = comm_util.get_session_login_name()
    db[TBL_ANNOTATING].update_one(
        {'login_name': login_name, 'batch_id': batch_id, 'dialogue.dialogue_id': dialogue_id},
        {"$set": {"dialogue.status": currentStatus}})

    dialogue_list = db[TBL_ANNOTATING].find({'login_name': login_name, "batch_id": batch_id})
    dialog_finish_num = 0
    dialog_total_num = 0
    for item in dialogue_list:
        dialogueObject = item["dialogue"]
        dialog_total_num += 1
        if 'FINISHED' == dialogueObject['status']:
            dialog_finish_num += 1

    batch_progress = format((dialog_finish_num / dialog_total_num), '.0%')
    db[TBL_BATCHSTATUS].update_one({'login_name': login_name},
                                   {"$set": {"annotating.$[elem].batch_progress": batch_progress}},
                                   array_filters=[{"elem.batch_id": batch_id}])

    responseObject = {
        "status": "success",
    }
    return jsonify(responseObject)


@annotating_bp.route("/turns", methods=["POST"])
def handle_turns():
    """
    POST - 加入新的Turn
    """
    data = request.get_json()
    query = data['query']
    domains = data['domains']

    responseObject = annotating_loader.generate_new_turn(query, domains['usr'], "", domains['sys'])

    return jsonify(responseObject)
