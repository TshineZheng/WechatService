# -*- coding:utf-8 -*-
import getopt
import json
import os
import sys
from threading import Thread

import itchat
from flask import Flask, make_response, Blueprint, Response

app = Flask(__name__)
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))

api = Blueprint('api', __name__, url_prefix='/api')

debug = True  # 调试模式

# 全局变量
g_qr_relative = 'static/qr.png'  # QR 保存的相对路径
g_qr_img_path = ''  # 二维码路径
g_qr_status: int = -1  # 二维码获取状态
g_is_login: bool = False  # 是否是登录状态

g_wechat_hot_reload = False


@api.route('/')
def hello_world():
    return 'Hello Flask!'


# 检测登陆状态
@api.route('/login/check', methods=["POST", "GET"])
def login_check():
    # return r(data={'login': g_is_login})
    return r(data={'login': g_is_login})


# 登陆
@api.route('/login')
def login():
    if g_is_login:
        log('已登陆，如需更换账号请先登出')
        return r(code=201, msg='已登陆，如需更换账号请先登出')

    itchat.logout()

    if os.path.exists(g_qr_img_path):
        log('QR 图片已存在，删除')
        os.remove(g_qr_img_path)

    wx_login_async()

    return r(msg='登陆请求已发送')


# 检测QR是否存在
@api.route('/qr/check', methods=["POST", "GET"])
def qr_check():
    if g_qr_status is -1:
        return r(code=201, msg='正在获取')

    if g_qr_status is 0:
        if os.path.exists(g_qr_img_path):
            return r(code=200, msg='QR已存在')
        else:
            return r(code=203, msg='QR已经获取到，但文件不存在：')

    return r(code=202, msg='二维码状态', data={'wechat_error_code': g_qr_status})


# 获取QR
@api.route('/qr')
def login_qr_code():
    path = g_qr_img_path
    if not os.path.exists(g_qr_img_path):
        log('QR文件不存在，使用默认图片代替')
        path = os.path.abspath(os.path.dirname(__file__)) + '/static/qr_failed.png'

    with open(path, 'rb') as f:
        image = f.read()

    return Response(image, mimetype='image/png')


# 登出
@api.route('/logout', methods=["POST", "GET"])
def logout():
    global g_is_login
    if g_is_login:
        g_is_login = False
        itchat.logout()
    return r(msg='已登出')


# 发送消息
@api.route('/send/<name>/<msg>')
def send_msg(name, msg):
    if g_is_login is False:
        if is_login() is False:
            return r(code=204, msg='未登入')

    try:
        namelist = itchat.search_friends(name=name)
        if len(namelist) <= 0:
            return r(code=203, msg='找不到联系人 ' + name)
        sendto = itchat.search_friends(name=name)[0]['UserName']
    except Exception as e:
        if hasattr(e, 'message'):
            return r(code=201, msg='查找联系人失败，原因：' + e.message)
        return r(code=201, msg='查找联系人失败')

    try:
        itchat.send_msg(msg, toUserName=sendto)
    except Exception as e:
        if hasattr(e, 'message'):
            return r(code=202, msg=u'发送消息失败，原因：' + e.message)
        return r(code=202, msg='发送消息失败')

    return r(msg='消息发送成功')


def r(status=200, code=200, data=None, msg='ok'):
    if data is None:
        data = {}
    return make_response(json.dumps({'code': code, 'data': data, 'msg': msg}, ensure_ascii=False), status, )


def my_async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


@my_async
def wx_login_async():
    global g_qr_status
    g_qr_status = -1
    itchat.auto_login(hotReload=g_wechat_hot_reload, qrCallback=qr_callback, loginCallback=login_callback,
                      exitCallback=exit_callback)


def qr_callback(uuid, status, qrcode):
    log('从微信返回 QR 信息 ，状态：' + status)
    global g_qr_status
    g_qr_status = int(status)
    if g_qr_status == 0:
        log('开始保存QR图片 = ' + g_qr_img_path)
        f = open(g_qr_img_path, 'wb')
        f.write(qrcode)
        f.close()
        log('QR图片保存成功')


def login_callback():
    global g_is_login
    g_is_login = True
    log('登录成功')
    pass


def exit_callback():
    global g_is_login
    g_is_login = False
    log('退出登陆')
    pass


def is_login():
    global g_is_login
    status = itchat.check_login()
    if status is 200:
        log('已登录')
        g_is_login = True
        return True
    log('未登录')
    g_is_login = False
    return g_is_login


def log(msg):
    if debug:
        print(msg)


def usage():
    print('''
--debug         是否打印日志
''')


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hd", ['help', 'debug'])
    except getopt.GetoptError:
        usage()
        sys.exit()
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-d', '--debug'):
            global debug
            debug = True

    img_folder = os.path.abspath(os.path.dirname(__file__))

    global g_qr_img_path
    g_qr_img_path = img_folder + "/" + g_qr_relative

    log("二维码路径  {p}".format(p=g_qr_img_path))

    app.run(port=6637, debug=debug)  # 设置debug=True是为了让代码修改实时生效，而不用每次重启加载


# 必须得放在 route 定义之后注册
app.register_blueprint(api)

if __name__ == '__main__':
    main(sys.argv[1:])
