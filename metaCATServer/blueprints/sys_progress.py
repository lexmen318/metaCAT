# -*- coding:utf-8 -*-
##############################################
#  SYSTEM PROGRESS Blueprint
##############################################
import os
from flask import jsonify, Blueprint
from utils.mongo_util import db
from comm_config import TBL_MEMBERS, TBL_BATCHSTATUS, DATA_VERSION, CURRENT_VERSION

sys_progress_bp = Blueprint('sys_progress', __name__)


@sys_progress_bp.route('/list', methods=['GET'])
def handle_sys_progress():
    # user_list = authenticate.registered_user_list()

    user_dict = {}
    users = db[TBL_MEMBERS].find({"user_role": "USER"})
    for user in users:
        user_dict[user["login_name"]] = user["user_name"]

    batch_list = []
    batch_status_list = db[TBL_BATCHSTATUS].find()
    for status_item in batch_status_list:
        login_name = status_item["login_name"]
        user_name = user_dict[login_name]

        for tag_item in status_item["annotating"]:
            batch_list.append({
                "login_name": login_name,
                "user_name": user_name,
                "category": "annotating",
                "batch_id": tag_item["batch_id"],
                "metadata_name": tag_item["metadata_name"],
                "batch_progress": tag_item["batch_progress"],
                "batch_description": tag_item["batch_description"]
            })

        for tag_item in status_item["paraphrasing"]:
            batch_list.append({
                "login_name": login_name,
                "user_name": user_name,
                "category": "paraphrasing",
                "batch_id": tag_item["batch_id"],
                "metadata_name": tag_item["metadata_name"],
                "batch_progress": tag_item["batch_progress"],
                "batch_description": tag_item["batch_description"]
            })

    return jsonify(batch_list)
