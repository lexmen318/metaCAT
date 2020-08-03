# -*- coding:utf-8 -*-
##############################################
#  BIG CAT SERVER
##############################################

from comm_config import TBL_BATCHSTATUS

# == Flask ==
from flask import Flask, jsonify, session, request, redirect, url_for, render_template, send_file
from flask_babel import Babel, refresh, gettext, ngettext
import logging
from flask_cors import CORS
from datetime import timedelta  # 导入过期时间库
from utils import comm_util
from utils.mongo_util import db
from blueprints.auth import auth_bp
from blueprints.sys_admin import sys_admin_bp
from blueprints.data_mgmt import data_mgmt_bp
from blueprints.sys_mgmt import sys_mgmt_bp
from blueprints.sys_progress import sys_progress_bp
from blueprints.sys_setting import sys_setting_bp
from blueprints.annotating import annotating_bp
from blueprints.paraphrasing import paraphrasing_bp
from blueprints.audio_recognition import asr_bp

import comm_setting

logging.basicConfig(level=logging.INFO)  # 设定log级别

# 全局初始化
comm_setting.init_global()


# 注册蓝图
def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(sys_admin_bp, url_prefix='/sys_admin')
    app.register_blueprint(data_mgmt_bp, url_prefix='/data_mgmt')
    app.register_blueprint(sys_mgmt_bp, url_prefix='/sys_mgmt')
    app.register_blueprint(sys_progress_bp, url_prefix='/sys_progress')
    app.register_blueprint(sys_setting_bp, url_prefix='/sys_setting')
    app.register_blueprint(annotating_bp, url_prefix='/annotating')
    app.register_blueprint(paraphrasing_bp, url_prefix='/paraphrasing')
    app.register_blueprint(asr_bp, url_prefix='/asr')


app = Flask(__name__)
babel = Babel(app, default_locale='zh')
# 注册蓝图
register_blueprints(app)

"""
    在flask当中使用 session 时，必须要做一个配置、
    即 flask的session中需要用到的秘钥字符串，可以是任意值
    flask默认把数据存放到了cookie中
"""
app.config["SECRET_KEY"] = 'g1=*w2%_vo5v7d&vec$@!0z@wpxd@3na*z-*c)*89u*8re2*2@'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 配置过期时间
# 为了避免跨域，关闭此设置
# app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config.from_object(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['LANGUAGES'] = {
    'en': 'English',
    'zh_CN': 'Chinese'
}
CORS(app)


@babel.localeselector
def get_locale():
    # if the user has set up the language manually it will be stored in the session,
    # so we use the locale from the user settings
    try:
        language = session['language']
    except KeyError:
        language = 'zh'
        session['language'] = language
    if language is not None:
        return language
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


@app.route('/language/<language>')
def change_language(language=None):
    # Get new user locale and timezone
    refresh()
    session['language'] = language
    result = {
        "status": True,
        "msg": gettext(u'SuccessfullyUpdate')
    }
    return jsonify(result)


@app.route("/")
def main():
    # 输出语言测试结果
    common_text = gettext(u'CurrentLanguage')
    format_text = ngettext(u'%(num)d formattedLanguageExample',
                           u'%(num)d anotherFormattedLanguageExample', 100)
    print("Current Language:=", common_text)
    print("Formatted language string example:=", format_text)

    return render_template('index.html')


@app.route("/batch_list_by_category", methods=['GET'])
def handle_batch_list_by_category():
    """
    GET - All batch metadata
    """
    batch_category = request.args.get('batch_category')
    login_name = comm_util.get_session_login_name()
    batch_info = db[TBL_BATCHSTATUS].find_one({'login_name': login_name})
    if batch_info == None:
        batch_list = []
    else:
        batch_list = batch_info[batch_category]
        batch_list = sorted(batch_list, key=lambda item: item['batch_id'])

    return jsonify(batch_list)


@app.route("/batch_description_post", methods=['POST'])
def handle_batch_description_post():
    # if request.method == "POST":
    data = request.get_json()
    batch_category = data['batch_category']
    batch_id = data['batch_id']
    batch_description = data['batch_description']

    login_name = comm_util.get_session_login_name()
    db[TBL_BATCHSTATUS].update_one({'login_name': login_name},
                                   {"$set": {batch_category + ".$[elem].batch_description": batch_description}},
                                   array_filters=[{"elem.batch_id": batch_id}])

    result = {
        "code": 200,
        "msg": gettext(u'SuccessfullyUpdate.')
    }
    return jsonify(result)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5013, debug=False, use_reloader=True)
    app.run(ssl_context='adhoc', host='0.0.0.0', port=5013, debug=False, use_reloader=True)
