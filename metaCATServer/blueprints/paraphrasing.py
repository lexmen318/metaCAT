# -*- coding:utf-8 -*-
##############################################
#  SYSTEM ADMIN Blueprint
##############################################
from comm_config import TBL_PARAPHRASING, TBL_BATCHSTATUS
from flask import jsonify, session, request, abort, Blueprint
from utils.mongo_util import db
from utils import comm_util, cache_util
from paraphrasing import paraphrasing_validator

paraphrasing_bp = Blueprint('paraphrasing', __name__)


def get_src_dialog(batch_id, dialogue_id, turn_id):
    """
    根据batch_id, dialog_id, turn_id查找src_dialog
    :param batch_id:
    :param dialog_id:
    :param turn_id:
    :return:
    """
    login_name = comm_util.get_session_login_name()

    # 从缓存中取出Dialogue
    cache_dialogue_key = cache_util.generate_dialogue_key(login_name, batch_id, dialogue_id)
    dialogue = cache_util.get(cache_dialogue_key)

    # 缓存中没有时从DB中获取Dialogue
    if dialogue == None:
        dialogue_query = {"login_name": login_name, "batch_id": batch_id, 'dialogue.dialogue_id': dialogue_id}
        dialogue = db[TBL_PARAPHRASING].find_one(dialogue_query)

    turn_list = dialogue['dialogue']['turn_list']
    for turn_item in turn_list:
        if turn_item['turn_id'] == turn_id:
            src_dialog = turn_item['src_dialog']
            break

    return src_dialog


def merge_dialog(batch_id, dialogue_id, para_turn_dict):
    login_name = comm_util.get_session_login_name()
    dialogue = db[TBL_PARAPHRASING].find_one(
        {"login_name": login_name, "batch_id": batch_id, 'dialogue.dialogue_id': dialogue_id})

    turn_list = dialogue["dialogue"]["turn_list"]
    for turn_item in turn_list:
        turn_id = turn_item["turn_id"]
        if para_turn_dict.__contains__(str(turn_id)):
            updated_para = para_turn_dict[str(turn_id)]
            turn_item['para_dialog'] = updated_para['para_dialog']

    return turn_list


@paraphrasing_bp.route("/validate_turn/<batch_id>/<dialogue_id>/<turn_id>", methods=["PUT"])
def handle_paraphrasing_validate_turn(batch_id, dialogue_id, turn_id):
    """
    校验一个对话轮次
    :param batch_id:
    :param id:
    :return:
    """

    turn = request.get_json()
    para_dialogue = turn['para_dialog']
    int_turn_id = int(turn_id)
    src_dialogue = get_src_dialog(batch_id, dialogue_id, int_turn_id)

    validate_result = paraphrasing_validator.validate_turn(src_dialogue, para_dialogue, turn['role'])
    return jsonify(validate_result)


@paraphrasing_bp.route("/validate_dialogues/<batch_id>/<dialogue_id>", methods=["PUT"])
def handle_paraphrasing_validate_dialogues(batch_id, dialogue_id):
    """
    校验对话轮次
    :param batch_id:
    :param id:
    :return:
    """

    para_turn_dict = request.get_json()
    turn_list = merge_dialog(batch_id, dialogue_id, para_turn_dict)
    validate_result = paraphrasing_validator.validate_dialogue(turn_list)
    # validate_result = {'status': 'success'}
    return jsonify(validate_result)


@paraphrasing_bp.route("/dialogues_main/<batch_id>", methods=["GET"])
def handle_paraphrasing_dialogues_main(batch_id):
    """
    GET - All dialogues
    DELETE - delete a dialogue
    """
    login_name = comm_util.get_session_login_name()
    dialogues = db[TBL_PARAPHRASING].find({"login_name": login_name, "batch_id": batch_id}) \
        .sort("dialogue.dialogue_id")

    responseObject = {}
    for item in dialogues:
        dialogue = item["dialogue"]
        # responseObject[dialogue["dialogue_id"]] = dialogue
        responseObject[dialogue["dialogue_id"]] = {
            "dialogue_id": dialogue["dialogue_id"],
            "turn_len": len(dialogue["turn_list"]),
            "finished": dialogue["para_info"]["finished"]
        }

    return jsonify(responseObject)


@paraphrasing_bp.route("/dialogues_detail/<batch_id>/<dialogue_id>", methods=["GET", "PUT", "DELETE"])
def handle_paraphrasing_dialogues_detail(batch_id, dialogue_id):
    """
    GET - get paraphrasing dialogues
    PUT - change specific dialogue with a dialogue
    :param batch_id:
    :param id:
    :return:
    """

    login_name = comm_util.get_session_login_name()
    dialogue = db[TBL_PARAPHRASING].find_one(
        {"login_name": login_name, "batch_id": batch_id, 'dialogue.dialogue_id': dialogue_id})

    # 生成缓存key
    cache_dialogue_key = cache_util.generate_dialogue_key(login_name, batch_id, dialogue_id)

    if not dialogue:
        responseObject = {"status": "failure",
                          "msg": "对话未找到, batch_id:=%s, dialogue_id:=%s" % (str(batch_id), str(dialogue_id))}
        return jsonify(responseObject)
    else:
        # 保存Dialogue到缓存中
        cache_util.put(cache_dialogue_key, dialogue)

    if request.method == "GET":
        responseObject = dialogue["dialogue"]
        task_list = responseObject["task_list"]
        for task_item in task_list:
            if '任务描述' in task_item.keys():
                task_item['TaskDescription'] = task_item['任务描述']
                # del task_item['任务描述']
        return jsonify(responseObject)

    if request.method == "PUT":

        para_turn_dict = request.get_json()

        # # 使用事务控制多级更新
        # with session.start_transaction():
        turn_finished_count = 0
        turn_list = dialogue["dialogue"]["turn_list"]
        for turn_item in turn_list:
            turn_id = turn_item["turn_id"]
            if para_turn_dict.__contains__(str(turn_id)):
                src_dialogue = turn_item['src_dialog']

                # 校验对话轮次
                updated_para = para_turn_dict[str(turn_id)]
                para_dialogue = updated_para['para_dialog']
                turn_validate_result = paraphrasing_validator.validate_turn(src_dialogue, para_dialogue, turn_item['role'])

                if turn_validate_result["status"] == 'SUCCESS':
                    turn_finished_count += 1
                    para_info = {
                        "status": turn_validate_result["status"],
                        "desc": "复述已完成"
                    }
                else:
                    para_info = {
                        "status": turn_validate_result["status"],
                        "desc": turn_validate_result["error"]
                    }

                db[TBL_PARAPHRASING].update_one(
                    {'login_name': login_name, "batch_id": batch_id, "dialogue.dialogue_id": dialogue_id},
                    {"$set": {"dialogue.turn_list.$[elem].para_dialog": para_dialogue,
                              "dialogue.turn_list.$[elem].para_info": para_info}},
                    array_filters=[{"elem.turn_id": turn_id}])

        # 整体统计
        if len(turn_list) == turn_finished_count:
            main_para_status = "FINISHED"
        else:
            main_para_status = "PROCESSING"

        main_para_info = {
            "total": len(turn_list),
            "finished": turn_finished_count,
            "status": main_para_status
        }
        db[TBL_PARAPHRASING].update_one(
            {'login_name': login_name, "batch_id": batch_id, "dialogue.dialogue_id": dialogue_id},
            {"$set": {"dialogue.activated": True,
                      "dialogue.para_info": main_para_info}})

        # 清除缓存中的dialogue
        cache_util.pop(cache_dialogue_key)

        responseObject = {"status": "SUCCESS"}

    if request.method == "DELETE":
        db[TBL_PARAPHRASING].delete_one(
            {'login_name': login_name, "batch_id": batch_id, "dialogue.dialogue_id": dialogue_id})
        responseObject = {"status": "SUCCESS"}

    # 计算dialogue完成比例
    dialogue_finished_count = 0
    dialogue_total_count = 0
    dialogue_list = db[TBL_PARAPHRASING].find({"login_name": login_name, "batch_id": batch_id})
    for dialogue in dialogue_list:
        dialogue_total_count += 1
        para_info = dialogue['dialogue']['para_info']
        if para_info['status'] == 'FINISHED':
            dialogue_finished_count += 1

    # 更新BatchStatus中的完成比例
    batch_progress = format((dialogue_finished_count / dialogue_total_count), '.0%')
    db[TBL_BATCHSTATUS].update_one({'login_name': login_name},
                                   {"$set": {"paraphrasing.$[elem].batch_progress": batch_progress}},
                                   array_filters=[{"elem.batch_id": batch_id}])

    return jsonify(responseObject)
