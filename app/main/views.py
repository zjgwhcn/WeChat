from flask import render_template, current_app, request
from . import main
from .. import motor, humaninfrared, humiture
import os
import RPi.GPIO as gpio
from ..wechatapi import *
import xml.etree.ElementTree as ET
from threading import Thread


class Servos:
    def __init__(self):
        gpio.setup(21, gpio.OUT)
        self.p = gpio.PWM(21, 50)
        self.p.start(0)

    def right(self):
        self.p.ChangeDutyCycle(2.5)
        time.sleep(0.2)
        self.p.ChangeDutyCycle(0)
        time.sleep(0.2)

    def left(self):
        self.p.ChangeDutyCycle(12.5)
        time.sleep(0.2)
        self.p.ChangeDutyCycle(0)
        time.sleep(0.2)

pin1 = 22
pin2 = 23
distance = 0
flag = True
flag_t = 0
flag_hand = False
servos = Servos()
channel = [24, 25, 5, 6]
speed = 10
frequency = 8

for i in channel:
    gpio.setup(i, gpio.OUT)

gpio.setup(pin1, gpio.OUT)
gpio.setup(pin2, gpio.OUT)

gpio.setup(26, gpio.OUT, initial=gpio.LOW)
gpio.setup(12, gpio.IN)

p1 = gpio.PWM(pin1, frequency)
p2 = gpio.PWM(pin2, frequency)

p1.start(speed)
p2.start(speed)


def speedplus():
    global speed
    stop()
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    speed += 10
    if speed > 100:
        speed = 100
    print(speed)
    p1.ChangeDutyCycle(speed)
    p2.ChangeDutyCycle(speed)


def speedreduce():
    global speed
    stop()
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    speed -= 10
    if speed < 10:
        speed = 10
    print(speed)
    p1.ChangeDutyCycle(speed)
    p2.ChangeDutyCycle(speed)


def up():
    global flag_t
    gpio.output(channel[0], gpio.HIGH)
    gpio.output(channel[2], gpio.HIGH)
    gpio.output(channel[1], gpio.LOW)
    gpio.output(channel[3], gpio.LOW)
    # if flag_t == 0:
    #     flag_t = 1
    t = Thread(target=auto_control)
    t.setDaemon(True)
    t.start()


def down():
    gpio.output(channel[1], gpio.HIGH)
    gpio.output(channel[3], gpio.HIGH)
    gpio.output(channel[0], gpio.LOW)
    gpio.output(channel[2], gpio.LOW)


def car_right():
    gpio.output(channel[3], gpio.LOW)
    gpio.output(channel[2], gpio.LOW)
    gpio.output(channel[1], gpio.LOW)
    gpio.output(channel[0], gpio.HIGH)
    time.sleep(0.5)
    stop()


def car_left():
    gpio.output(channel[1], gpio.LOW)
    gpio.output(channel[0], gpio.LOW)
    gpio.output(channel[3], gpio.LOW)
    gpio.output(channel[2], gpio.HIGH)
    time.sleep(0.5)
    stop()


def stop():
    global flag, flag_t
    flag = False
    for i in channel:
        gpio.output(i, gpio.LOW)
    time.sleep(1)
    flag = True
    flag_t = 0


def get_distance():
    t1, t2 = 0, 0
    gpio.output(26, gpio.HIGH)
    time.sleep(0.000015)
    gpio.output(26, gpio.LOW)
    while True:
        if gpio.input(12):
            t1 = time.time()
            break
    while True:
        if not gpio.input(12):
            t2 = time.time()
            break
    # print((t2 - t1) * 340 / 2)
    distance = float((t2 - t1) * 340 / 2)
    return distance


def auto_control():
    global flag, flag_hand
    while flag:
        if get_distance() < 0.2:
            stop()
            flag_hand = False
            flag = False
        else:
            continue
    if flag_hand:
        pass
    else:
        global servos
        servos.left()
        distance_left = get_distance()
        servos.right()
        servos.right()
        distance_right = get_distance()
        servos.left()
        if distance_left > distance_right:
            car_left()
        else:
            car_right()

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
        if fromUser != 'oq8wpxE9mj9lZr8JjlgMKa1ZMTTw':
            return render_template('text.xml',toUser=fromUser,fromUser=toUser,createtime=int(time.time()),content='对不起，你没有权限！')
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
    if get_distance() > 0.2:
        up()
    else:
        pass
    return '0'


@main.route('/movedown')
def movedown():
    down()
    return '0'


@main.route('/carleft')
def carleft():
    car_left()
    return '0'


@main.route('/carright')
def carright():
    car_right()
    return '0'


@main.route('/carstop')
def carstop():
    global flag_hand
    flag_hand = True
    stop()
    return '0'


@main.route('/plus')
def plusspeed():
    speedplus()
    return '0'


@main.route('/reduce')
def reducespeed():
    speedreduce()
    return '0'
