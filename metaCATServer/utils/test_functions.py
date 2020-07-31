import zipfile
import shutil
import os

import utils

__DEFAULT_PATH = "LIDA_ANNOTATIONS"


# def compress_folder(zipfile_name, zip_folder):
#     # 压缩错误文件
#     with zipfile.ZipFile(zipfile_name, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
#         files = os.listdir(zip_folder)
#         for file in files:
#             file_namepath = zip_folder + '/' + file
#             zip_ref.write(file_namepath, os.path.basename(file_namepath))
#
#
# # error_key = utils.get_time_keyword()
# error_key = '20200428184648'
# error_path = __DEFAULT_PATH + '/error/' + error_key
# error_zipfile = error_path + '.zip'
#
# compress_folder(error_zipfile, error_path)

# dialogues = utils.load_json_file('test/20200428095044014.json')
# print(dialogues)

import os

local_filename = "/root/path/treee"
filename = os.path.split(local_filename)[1]
print(filename)
