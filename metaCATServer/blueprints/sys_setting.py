# -*- coding:utf-8 -*-
##############################################
#  SYSTEM PROGRESS Blueprint
##############################################
import os
from flask import request, jsonify, Blueprint
from utils.mongo_util import db
from utils import sysInit_util
from comm_config import TBL_CAT_CONFIG, DATA_VERSION, CURRENT_VERSION

sys_setting_bp = Blueprint('sys_setting', __name__)


@sys_setting_bp.route('/view', methods=['GET'])
def handle_sys_setting_view():
    """
    取得系统设置
    :return:
    """
    sys_setting = sysInit_util.get_sys_setting()
    config = sys_setting['config']
    return jsonify(config)


@sys_setting_bp.route("/change", methods=["POST"])
def handle_sys_setting_change():
    """
    POST - 更新系统设置
    """
    data = request.get_json()
    config = data['config']

    sysInit_util.update_sys_setting(config)

    responseObject = {"status": "SUCCESS"}

    return jsonify(responseObject)
