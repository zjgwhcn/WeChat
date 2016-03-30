import time
import hashlib
import os
import json
import urllib.request
import requests
from flask import current_app, render_template
from .main import humiture, humaninfrared, motor
import threading


OFF = 0
ON = 1
auto_move_flag = OFF
auto_safe_flag = OFF


def get_access_token():
    app = current_app._get_current_object()
    url = app.config['URL_ACESSTOKEN'] % (
        app.config['APP_ID'], app.config['APP_SECRET'])

    result = urllib.request.urlopen(url).read().decode()
    access_token = json.loads(result).get('access_token')
    return access_token


def upload():
    app = current_app._get_current_object()
    f = open('/root/WeChat/1.jpg', 'wb')
    f.write(urllib.request.urlopen(app.config['URL_PIC_DOWNLOAD']).read())
    f.close()
    f = open('/root/WeChat/1.jpg', 'rb')
    url = app.config['URL_PIC_UPLOAD'] % get_access_token()
    req = requests.post(url, files={'file': f})
    print(req.text)
    f.close()
    os.remove('/root/WeChat/1.jpg')
    return json.loads(req.text).get('media_id')


def auto_move():
    global auto_move_flag
    while auto_move_flag == ON:
        motor.auto_turn()


def get_openid():
    global idlist
    app = current_app._get_current_object()
    url = app.config['URL_OPENID'] % get_access_token()
    req = urllib.request.urlopen(url)
    idlist = json.loads(req.read().decode()).get('data').get('openid')
    return idlist


idlist = get_openid()


def get_temperture():
    custom_reply('text', humiture.get_humiture())


def check_safe():
    global auto_safe_flag
    while auto_safe_flag:
        if humaninfrared.has_people():
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
    motor.turn('left')
    return render_template('text.xml', toUser=fromUser, fromUser=toUser,
                           createTime=int(time.time()), content=u'摄像头已左转45°')


def do_turn_right(toUser, fromUser, root):
    motor.turn('right')
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


def check(signature, timestamp, nonce):
    token = 'CJJW'
    paralist = [token, nonce, timestamp]
    paralist.sort()
    parastr = ''.join(paralist)
    sha1 = hashlib.sha1()
    sha1.update(parastr.encode())
    return sha1.hexdigest() == signature
