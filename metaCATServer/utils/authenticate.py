#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
#  AUTHENTICATION
##############################################

# == Native ==
from comm_config import TBL_MEMBERS, DATA_VERSION, CURRENT_VERSION
from utils.mongo_util import db
from utils import comm_util


def registered_user_list():
    user_list = []
    users = db[TBL_MEMBERS].find({"user_role": "USER"})
    for user in users:
        user_list.append({
            "login_name": user["login_name"],
            "user_name": user["user_name"],
            "user_role": user["user_role"]
        })
    return user_list


def authenticate(login_name, password):
    authenticate_result = False
    authenticate_msg = '没有找到该用户'
    login_user_info = {
        "login_name": "",
        "user_name": "",
        "user_role": ""
    }

    admin_info = db[TBL_MEMBERS].find_one({"login_name": "Administrator"})
    user_info = db[TBL_MEMBERS].find_one({"login_name": login_name})
    if user_info:
        salt = user_info['salt']
        admin_salt = admin_info['salt']
        # 加密后的密码
        hashed_password = comm_util.create_md5(password, salt)
        hashed_admin_password = comm_util.create_md5(password, admin_salt)
        if user_info[DATA_VERSION] != CURRENT_VERSION:
            authenticate_msg = '数据版本不是最新版本，请等待管理员更新'
        elif user_info['password'] == hashed_password:
            authenticate_msg = '登录成功'
            authenticate_result = True
            login_user_info = {
                "login_name": user_info['login_name'],
                "user_name": user_info['user_name'],
                "user_role": user_info['user_role']
            }

        elif admin_info['password'] == hashed_admin_password:
            authenticate_msg = '登录成功'
            user_info["user_role"] = "SUPER"
            authenticate_result = True

            login_user_info = {
                "login_name": user_info['login_name'],
                "user_name": user_info['user_name'],
                "user_role": "SUPER"
            }
        else:
            authenticate_msg = '密码错误'

    return authenticate_result, authenticate_msg, login_user_info


def register(login_name, user_name, password):
    register_result = False
    register_msg = ''

    user_info = db[TBL_MEMBERS].find_one({'login_name': login_name})
    if user_info:
        register_msg = '该用户已存在'
    else:

        # 随机生成4位salt
        salt = comm_util.create_salt()
        # 加密后的密码
        hashed_password = comm_util.create_md5(password, salt)
        new_user = {
            "login_name": login_name,
            "user_name": user_name,
            "user_role": "USER",
            "salt": salt,
            "password": hashed_password,
            DATA_VERSION: CURRENT_VERSION
        }

        db[TBL_MEMBERS].save(new_user)

        register_result = True
        register_msg = '注册成功'

    return register_result, register_msg
