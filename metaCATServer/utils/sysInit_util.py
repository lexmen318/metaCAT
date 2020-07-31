# -*- coding:utf-8 -*-
##############################################
#  SYSTEM INITIALIZATION
##############################################
from utils.mongo_util import db
from utils import comm_util
from comm_config import TBL_CAT_CONFIG, TBL_MEMBERS, DATA_VERSION, CURRENT_VERSION, \
    ADMIN_LOGIN_NAME, ADMIN_ROLE, ADMIN_DEFAULT_PWD, ADMIN_DEFAULT_SALT


def init_admin():
    admin_info = db[TBL_MEMBERS].find_one({"login_name": ADMIN_LOGIN_NAME})
    if admin_info:
        print("管理员用户已经存在")
    else:
        admin_user = db[TBL_MEMBERS].insert_one(
            {
                "login_name": ADMIN_LOGIN_NAME,
                "password": ADMIN_DEFAULT_PWD,
                "salt": ADMIN_DEFAULT_SALT,
                "user_name": "管理员",
                "user_role": ADMIN_ROLE,
                DATA_VERSION: CURRENT_VERSION
            }
        )
        print("增加管理员用户")


def change_admin_pwd(oldPassWord, password):
    result = {"status": "success", "msg": "设置成功"}

    admin_info = db[TBL_MEMBERS].find_one({"login_name": ADMIN_LOGIN_NAME})
    admin_salt = admin_info['salt']

    # 加密后的密码
    hashed_old_password = comm_util.create_md5(oldPassWord, admin_salt)

    if admin_info['password'] != hashed_old_password:
        result = {"status": "fail", "msg": "原始密码不正确"}
    else:
        # 随机生成新salt,并加密密码
        new_salt = comm_util.create_salt()
        hashed_admin_password = comm_util.create_md5(password, new_salt)

        db[TBL_MEMBERS].update_one(
            {'login_name': ADMIN_LOGIN_NAME},
            {"$set": {"salt": new_salt, "password": hashed_admin_password}})

    return result


def get_sys_setting():
    sys_setting = db[TBL_CAT_CONFIG].find_one({"config_name": "general"})
    return sys_setting


def sys_setting_init():
    # 系统设置初始化
    sys_setting = get_sys_setting()
    if sys_setting:
        pass
    else:
        # 无初始化设置时
        big_config = {
            "config_name": "general",
            "config": {
                "annotating": {
                    "sysAnnotating": True,
                    "turnDeleteFlag": True,
                    "turnAddFlag": True
                },
                "paraphrasing": {
                    "asrOption": False
                }
            }
        }
        db[TBL_CAT_CONFIG].save(big_config)


def update_sys_setting(config):
    db[TBL_CAT_CONFIG].update_one(
        {'config_name': "general"},
        {"$set": {"config": config}})
