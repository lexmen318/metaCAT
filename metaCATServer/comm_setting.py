# -*- coding:utf-8 -*-
##############################################
#  COMMON SETTING
##############################################
from utils import sysInit_util
# def init_metadata():
#     # 生成Metadata缓存key, 放入缓存
#     metadata_annotating_list = db[TBL_METADATA].find()
#     for metadata in metadata_annotating_list:
#         medatadata_key = cache_util.generate_medatadata_key(metadata['category'], metadata['metadata_name'])
#         cache_util.put(medatadata_key, metadata['metadata_value'])
#
#     print('全局缓存完成')


def init_global():
    # 创建初始管理员
    sysInit_util.init_admin()

    # 系统设置初始化
    sysInit_util.sys_setting_init()
    # 全局设置及缓存
    # init_metadata()
