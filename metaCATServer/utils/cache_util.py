# -*- coding:utf-8 -*-
##############################################
#  CACHE UTILITY
##############################################

# 默认系统路径设置
__CACHE = {}


def generate_medatadata_key(medatadata_category, medatadata_name):
    """
    generate medatadata_key in cache
    :param medatadata_category:
    :param medatadata_name:
    :return:
    """
    medatadata_key = "{}-{}".format(medatadata_category, medatadata_name)
    return medatadata_key


def generate_dialogue_key(login_name, batch_id, dialogue_id):
    """
    generate dialogue_key in cache
    :param login_name:
    :param batch_id:
    :param dialogue_id:
    :return:
    """
    cache_dialogue_key = "{}-{}-{}".format(login_name, batch_id, dialogue_id)
    return cache_dialogue_key


def put(key, value):
    """
    加入缓存
    :param key:
    :param value:
    :return:
    """
    __CACHE[key] = value


def get(key):
    """
    取出缓存
    :param key:
    :return:
    """
    if key in __CACHE.keys():
        value = __CACHE[key]
        return value
    else:
        return None


def pop(key):
    """
    删除缓存
    :param key:
    :return:
    """
    __CACHE.pop(key)
