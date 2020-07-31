# -*- coding:utf-8 -*-
##############################################
#  语音识别（ASR | Automatic Speech Recognition）
##############################################
from flask import jsonify, request, Blueprint
import os
import base64
from comm_config import __DEFAULT_PATH
from utils import comm_util

asr_bp = Blueprint('asr', __name__)


@asr_bp.route("/audio_recognize", methods=['POST'])
def handle_audio_recognize():
    audio = request.form['audio']
    audio_content = '默认无ASR服务集成'

    # 若需调试，可输出音频文件
    # export_audio(audio)

    # recognizer = ASRRecognizer()  # 初始化识别器
    # audio_content = recognizer.audio_recognize(audio)  # 发送识别请求

    result = {
        "data": audio_content
    }
    return jsonify(result)


def export_audio(audio):
    """
    输出音频文件
    :param audio:
    :return:
    """

    audio_b64decode = base64.b64decode(audio, ' /')

    # 创建音频文件保存路径
    audio_path = __DEFAULT_PATH + '/audio'
    comm_util.create_dirs(audio_path)

    audio_key = comm_util.get_time_keyword()
    audio_file_name = os.path.join(audio_path, audio_key + ".wav")

    with open(audio_file_name, 'wb') as pcm:
        pcm.write(audio_b64decode)
