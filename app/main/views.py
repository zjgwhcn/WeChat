from flask import render_template, current_app, request
from . import main
from .. import motor, humaninfrared, humiture, car
import os
from ..wechatapi import *
import xml.etree.ElementTree as ET


@main.route('/weixin', methods=['GET', 'POST'])
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


@main.route('/')
def monitor():
    shutdown()
    return render_template('index.html')


@main.route('/left')
def left():
    motor.turn('left')
    return '0'


@main.route('/right')
def right():
    motor.turn('right')
    return '0'


@main.route('/closelight')
def myclose():
    os.system('irsend SEND_ONCE light key_close')
    return '0'


@main.route('/openlight')
def myopen():
    os.system('irsend SEND_ONCE light key_open')
    return '0'


@main.route('/lightup')
def lightup():
    os.system('irsend SEND_ONCE light key_up')
    return '0'


@main.route('/lightdown')
def lightdown():
    os.system('irsend SEND_ONCE light key_down')
    return '0'


@main.route('/moveup')
def moveup():
    if car.get_distance() > 0.5:
        print('hehe')
        car.up()
    else:
        pass
    return '0'


@main.route('/movedown')
def movedown():
    car.down()
    return '0'


@main.route('/carleft')
def carleft():
    car.left()
    return '0'


@main.route('/carright')
def carright():
    car.right()
    return '0'


@main.route('/carstop')
def carstop():
    car.stop()
    return '0'


@main.route('/plus')
def plusspeed():
    car.speedplus()
    return '0'


@main.route('/reduce')
def reducespeed():
    car.speedreduce()
    return '0'
