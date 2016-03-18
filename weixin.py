from flask import Flask, request, render_template
from flask.ext.script import Manager
import time
import hashlib
import os
import json
import xml.etree.ElementTree as ET
import urllib.request
import requests
import module
import threading
import car

app = Flask(__name__)
app.debug = True

manager = Manager(app)

OFF = 0
ON = 1
auto_move_flag = OFF
auto_safe_flag = OFF


def get_access_token():
    AppID = 'wx6b11c0a7c39c89bb'
    AppSecret = 'f8dce47284bab8aa55e1ffd7798eab39'
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
        AppID, AppSecret)

    result = urllib.request.urlopen(url).read().decode()
    access_token = json.loads(result).get('access_token')
    return access_token


def upload():
    f = open('/root/WeChat/1.jpg', 'wb')
    f.write(urllib.request.urlopen(
        'http://192.168.199.135:8080/?action=snapshot').read())
    f.close()
    f = open('/root/WeChat/1.jpg', 'rb')
    url = 'https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=image' % get_access_token()
    req = requests.post(url, files={'file': f})
    print(req.text)
    f.close()
    os.remove('/root/WeChat/1.jpg')
    return json.loads(req.text).get('media_id')


def auto_move():
    global auto_move_flag
    while auto_move_flag == ON:
        module.on()


def get_openid():
    global idlist
    url = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid' % get_access_token()
    req = urllib.request.urlopen(url)
    idlist = json.loads(req.read().decode()).get('data').get('openid')
    return idlist


idlist = get_openid()


def get_temperture():
    custom_reply('text', module.get_temperature())


def check_safe():
    global auto_safe_flag
    while auto_safe_flag:
        if module.check():
            custom_reply('text', '有人进入监控范围')
            custom_reply('img', upload())


def custom_reply(msgType, content):
    global idlist
    url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s' % get_access_token()

    def text(content):
        for id in idlist:
            data = {
                "touser": id,
                "msgtype": "text",
                "text": {
                    "content": content
                }
            }

            req = urllib.request.Request(url)
            req.add_header('Context-Type', 'application/json')
            req.add_header('encoding', 'utf-8')

            response = urllib.request.urlopen(
                req, json.dumps(data, ensure_ascii=False).encode())
            print(response.read())

    def img(content):
        for id in idlist:
            data = {
                "touser": id,
                "msgtype": "image",
                "image": {
                    "media_id": content
                }
            }
            req = urllib.request.Request(url)
            req.add_header('Context-Type', 'application/json')
            req.add_header('encoding', 'utf-8')

            response = urllib.request.urlopen(
                req, json.dumps(data, ensure_ascii=False).encode())
            print(response.read())

    reply = {
        'text': text,
        'img': img
    }

    reply[msgType](content)


def recv_text(toUser, fromUser, root):
    content = root.find('Content').text
    return reply_text(toUser, fromUser, content)


def recv_event(toUser, fromUser, root):
    event = root.find('Event').text
    return event_type[event](toUser, fromUser, root)


def reply_subscribe(toUser, fromUser, root):
    return render_template('text.xml', toUser=fromUser, fromUser=toUser,
                           createTime=int(time.time()), content=u'您好，欢迎关注CJJW!')


def reply_unsubscribe(toUser, fromUser, root):
    return '0'


def reply_click(toUser, fromUser, root):
    eventKey = root.find('EventKey').text
    return click_type[eventKey](toUser, fromUser, root)


def reply_view(toUser, fromUser, root):
    return '0'


def reply_text(toUser, fromUser, content):
    return render_template('text.xml', toUser=fromUser, fromUser=toUser,
                           createTime=int(time.time()), content=content)


def do_get_temperture(toUser, fromUser, root):
    t = threading.Thread(target=get_temperture)
    t.start()
    return render_template('text.xml', toUser=fromUser, fromUser=toUser,
                           createTime=int(time.time()), content=u'正在获取温湿度,请稍后...')


def do_screen_shot(toUser, fromUser, root):
    return render_template('image.xml', toUser=fromUser, fromUser=toUser,
                           createTime=int(time.time()), media_id=upload())


def do_auto_safe_on(toUser, fromUser, root):
    global auto_safe_flag
    if auto_safe_flag == OFF:
        auto_safe_flag = ON
        t = threading.Thread(target=check_safe)
        t.start()
        return render_template('text.xml', toUser=fromUser, fromUser=toUser,
                               createTime=int(time.time()), content=u'安全预警功能已开启')
    else:
        return render_template('text.xml', toUser=fromUser, fromUser=toUser,
                               createTime=int(time.time()), content=u'安全预警功能早已开启')


def do_auto_safe_off(toUser, fromUser, root):
    global auto_safe_flag
    if auto_safe_flag == ON:
        auto_safe_flag = OFF
        return render_template('text.xml', toUser=fromUser, fromUser=toUser,
                               createTime=int(time.time()), content=u'安全预警功能已关闭')
    else:
        return render_template('text.xml', toUser=fromUser, fromUser=toUser,
                               createTime=int(time.time()), content=u'安全预警功能并未开启，不需要关闭')


def do_turn_left(toUser, fromUser, root):
    module.turn('left')
    return render_template('text.xml', toUser=fromUser, fromUser=toUser,
                           createTime=int(time.time()), content=u'摄像头已左转45°')


def do_turn_right(toUser, fromUser, root):
    module.turn('right')
    return render_template('text.xml', toUser=fromUser, fromUser=toUser,
                           createTime=int(time.time()), content=u'摄像头已右转45°')


def do_auto_move_on(toUser, fromUser, root):
    global auto_move_flag
    if auto_move_flag == OFF:
        auto_move_flag = ON
        t = threading.Thread(target=auto_move)
        t.start()
        return render_template('text.xml', toUser=fromUser, fromUser=toUser,
                               createTime=int(time.time()), content=u'摄像头自动旋转已开启')
    else:
        return render_template('text.xml', toUser=fromUser, fromUser=toUser,
                               createTime=int(time.time()), content=u'摄像头自动旋转早已开启')


def do_auto_move_off(toUser, fromUser, root):
    global auto_move_flag
    if auto_move_flag == ON:
        auto_move_flag = OFF
        return render_template('text.xml', toUser=fromUser, fromUser=toUser,
                               createTime=int(time.time()), content=u'摄像头自动旋转已关闭')
    else:
        return render_template('text.xml', toUser=fromUser, fromUser=toUser,
                               createTime=int(time.time()), content=u'摄像头自动旋转并未开启，不需要关闭')


rec_type = {
    'text': recv_text,
    'event': recv_event
}

event_type = {
    'subscribe': reply_subscribe,
    'unsubcribe': reply_unsubscribe,
    'CLICK': reply_click,
    'VIEW': reply_view
}

click_type = {
    'V1001_TEMPERATURE': do_get_temperture,
    "V1001_SCREENSHOT": do_screen_shot,
    "V1001_AUTOSAFE_ON": do_auto_safe_on,
    "V1001_AUTOSAFE_OFF": do_auto_safe_off,
    "V1001_LEFT": do_turn_left,
    "V1001_RIGHT": do_turn_right,
    "V1001_AUTOMOVE_ON": do_auto_move_on,
    "V1001_AUTOMOVE_OFF": do_auto_move_off
}


@app.route('/weixin', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        data = request.args
        echostr = data['echostr']
        signature = data['signature']
        timestamp = data['timestamp']
        nonce = data['nonce']
        if check(signature, timestamp, nonce):
            return echostr
    else:
        rec = request.data
        root = ET.fromstring(rec)
        msgType = root.find('MsgType').text
        toUser = root.find('ToUserName').text
        fromUser = root.find('FromUserName').text
        try:
            return rec_type[msgType](toUser, fromUser, root)
        except KeyError:
            return render_template('text.xml', toUser=fromUser, fromUser=toUser,
                                   createTime=int(time.time()), content=u'此功能正在开发中')


@app.route('/')
def monitor():
    return render_template('index.html')


@app.route('/left')
def left():
    module.turn('left')
    return '0'


@app.route('/right')
def right():
    module.turn('right')
    return '0'


@app.route('/closelight')
def myclose():
    os.system('irsend SEND_ONCE light key_close')
    return '0'


@app.route('/openlight')
def myopen():
    os.system('irsend SEND_ONCE light key_open')
    return '0'


@app.route('/lightup')
def up():
    os.system('irsend SEND_ONCE light key_up')
    return '0'


@app.route('/lightdown')
def mydown():
    os.system('irsend SEND_ONCE light key_down')
    return '0'

@app.route('/movetup')
def up():
    car.up()
    return '0'


@app.route('/movedown')
def mydown():
    car.down()
    return '0'

@app.route('/carleft')
def left():
    car.left()
    return '0'


@app.route('/carright')
def right():
    car.right()
    return '0'

@app.route('/carstop')
def right():
    car.stop()
    return '0'


def check(signature, timestamp, nonce):
    token = 'CJJW'
    paralist = [token, nonce, timestamp]
    paralist.sort()
    parastr = ''.join(paralist)
    sha1 = hashlib.sha1()
    sha1.update(parastr.encode())
    return sha1.hexdigest() == signature


manager.run()
