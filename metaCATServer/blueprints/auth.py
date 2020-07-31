# -*- coding:utf-8 -*-
##############################################
#  AUTHENTICATION Blueprint
##############################################

from flask import jsonify, session, request, abort, Blueprint
from flask_babel import gettext

from utils.mongo_util import db
from utils import authenticate
from utils import comm_util
from utils import sysInit_util
from comm_config import TBL_MEMBERS, TBL_BATCHSTATUS, TBL_ANNOTATING, TBL_PARAPHRASING, \
    DATA_VERSION, CURRENT_VERSION

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login", methods=['POST'])
def handle_login():
    data = request.get_json()
    login_name = data['login_name']
    password = data['password']

    authenticate_result, authenticate_msg, user_info = authenticate.authenticate(login_name, password)
    if authenticate_result:
        """设置session的数据"""
        session["metacat_login_name"] = login_name
        session["metacat_user_info"] = user_info

    result = {
        "authenticate_result": authenticate_result,
        "authenticate_msg": authenticate_msg,
        "user_info": user_info
    }
    return jsonify(result)


@auth_bp.route("/logout", methods=['POST'])
def handle_logout():
    session.pop('metacat_user_info', None)  # 删除session
    result = {
        "authenticate_result": True,
        "authenticate_msg": gettext(u'msgUserLogout')
    }
    return jsonify(result)


@auth_bp.route("/register", methods=['POST'])
def handle_register():
    data = request.get_json()
    login_name = data['login_name']
    user_name = data['user_name']
    password = data['password']
    register_result, register_msg = authenticate.register(login_name, user_name, password)

    if register_result:
        # 创建新的batch状态列表
        default_batch_status = comm_util.generate_default_batchstatus(login_name)
        db[TBL_BATCHSTATUS].save(default_batch_status)

    result = {
        "register_result": register_result,
        "register_msg": register_msg
    }
    return jsonify(result)

@auth_bp.route("/change_admin_pwd", methods=['POST'])
def handle_change_admin_pwd():

    data = request.get_json()
    oldPassWord = data['oldPassWord']
    password = data['password']
    confirmPassWord = data['confirmPassWord']

    result = {"status": "success", "msg": gettext(u'msgSettingSuccess')}

    if password != confirmPassWord:
        result = {"status": "fail", "msg": gettext(u'msgConfirmPasswordError')}
    else:
        result = sysInit_util.change_admin_pwd(oldPassWord, password)

    return jsonify(result)
