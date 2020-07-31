# -*- coding:utf-8 -*-

################################################################################
# IMPORTS
################################################################################
import os
import json
from typing import Dict, List, Any, Tuple, Hashable, Iterable, Union
import datetime
import time
import zipfile
import shutil
import hashlib, random
from comm_config import TERM_ANNOTATING, TERM_PARAPHRASING, \
    DATA_VERSION, CURRENT_VERSION
from flask import session


################################################################################
# CODE
################################################################################
def load_json_file(path: str) -> Any:
    """Loads a JSON file."""
    with open(path, "r", encoding='utf-8') as f:
        content = json.load(f)
    return content


def save_json_file(obj: Any, path: str) -> None:
    """Saves a JSON file."""
    with open(path, "w", encoding='utf-8') as f:
        json.dump(obj, f, indent=2)


def save_json_cn_file(obj: Any, path: str) -> None:
    """Saves a JSON file."""
    with open(path, "w", encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


def save_txt_file(lines, path: str) -> None:
    """Saves a JSON file."""
    with open(path, "w", encoding='utf-8') as f:
        for line in lines:
            f.write(line + "\n")

# 获取由4位随机大小写字母、数字组成的salt值
def create_salt(length=4):
    salt = ''.join([chr(random.randint(48, 122)) for i in range(20)])
    return salt


# 获取原始密码+salt的md5值
def create_md5(pwd, salt):
    conbin_pass = pwd + salt
    return hashlib.md5(conbin_pass.encode('utf-8')).hexdigest()

def get_time_keyword():
    time_keyword = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
    return time_keyword


def get_timestamp_key():
    current_milli_time = int(round(time.time() * 1000))
    return str(current_milli_time)


def get_time_stamp():
    time_stamp = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    return time_stamp


def get_session_login_name():
    """
    从session中取出用户名
    :return:
    """
    login_name = session.get("metacat_login_name")
    # print(login_name)
    return login_name


def create_dirs(path):
    """
    批量创建目录
    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)


def uncompress_file(zipfile_name, unzip_folder):
    """
    解压缩文件
    :param zipfile_name:
    :param unzip_folder:
    :return:
    """
    with zipfile.ZipFile(zipfile_name, 'r') as zip_ref:
        zip_ref.extractall(unzip_folder)


def compress_folder(zipfile_name, zip_folder):
    """
    压缩文件夹
    :param zipfile_name:
    :param zip_folder:
    :return:
    """
    with zipfile.ZipFile(zipfile_name, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        for root, dirs, files in os.walk(zip_folder):
            for raw_filename in files:
                file_namepath = root + '/' + raw_filename
                arcname = file_namepath.replace(zip_folder, '')
                # arcname = os.path.basename(file_namepath)
                zip_ref.write(file_namepath, arcname)

        # files = os.listdir(zip_folder)
        # for file in files:
        #     file_namepath = zip_folder + '/' + file
        #     zip_ref.write(file_namepath, os.path.basename(file_namepath))


def rm_file(file_name):
    """
    检查并删除文件
    :param file_name:
    :return:
    """
    if os.path.exists(file_name):
        os.remove(file_name)


def rm_folder_tree(folder_name):
    """
    删除文件夹
    :param folder_name:
    :return:
    """
    try:
        shutil.rmtree(folder_name, ignore_errors=True)
    except Exception as e:
        print('Removing Files fails, INFO: %s' % str(e))


def generate_default_batchstatus(login_name):
    """
    根据用户登录名生成默认的batchStatus
    :param login_name:
    :return:
    """
    batch_status = {"login_name": login_name, TERM_ANNOTATING: [], TERM_PARAPHRASING: [], DATA_VERSION: CURRENT_VERSION}
    return batch_status
# EOF
