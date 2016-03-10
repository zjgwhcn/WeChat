import RPi.GPIO as gpio
import time

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)


def startSignal(channel):
    # 发送开始信号

    gpio.setup(channel, gpio.OUT)
    gpio.output(channel, gpio.LOW)
    time.sleep(0.2)
    gpio.output(channel, gpio.HIGH)


def getData(channel):
    time.sleep(1)
    data = []
    j = 0

    startSignal(channel)
    time.sleep(0.5)
    startSignal(channel)

    # 等待dht11回应
    gpio.setup(channel, gpio.IN)

    while gpio.input(channel) == gpio.LOW:
        continue

    while gpio.input(channel) == gpio.HIGH:
        continue

    while j < 40:
        k = 0
        j += 1
        while gpio.input(channel) == gpio.LOW:
            continue

        while gpio.input(channel) == gpio.HIGH:
            k += 1
            if k > 100:
                break

        if k < 8:
            data.append(0)
        else:
            data.append(1)

    print("sensor working!")

    # 数据解析
    humidity_bit = data[0:8]
    humidity_point_bit = data[8:16]
    temperature_bit = data[16:24]
    temperature_point_bit = data[24:32]
    check_bit = data[32:40]

    humidity = 0
    humidity_point = 0
    temperature = 0
    temperature_point = 0
    check = 0

    for i in range(8):
        humidity += humidity_bit[i] * 2**(7 - i)
        humidity_point += humidity_point_bit[i] * 2**(7 - i)
        temperature += temperature_bit[i] * 2**(7 - i)
        temperature_point += temperature_point_bit[i] * 2**(7 - i)
        check += check_bit[i] * 2**(7 - i)

    tmp = humidity + humidity_point + temperature + temperature_point
    if check == tmp:
        #print ("当前温度为%d℃,相对湿度为%d%" % (temperature,humidity))
        return (u"当前温度为%d℃,相对湿度为%d%%") % (temperature, humidity)
    else:
        return getData(channel)
    # gpio.cleanup()


def get_temperature():
    channel = 12
    return getData(channel)


def check():

    channel = 11
    # time.sleep(60)
    # gpio.setup(channel,gpio.OUT)
    # gpio.output(channel,gpio.HIGH)
    gpio.setup(channel, gpio.IN)
    if gpio.input(channel):
        gpio.cleanup()
        return 1
    else:
        return 0


def turn(direction):

    channel = [40, 38, 36, 35]

    arr = [0, 1, 2, 3]

    if direction == 'left':
        arr = [3, 2, 1, 0]

    for i in channel:
        gpio.setup(i, gpio.OUT)
        gpio.output(i, False)

    # 64   angle= 45
    for x in range(0, 64):
        for i in arr:
            time.sleep(0.01)
            for j in range(0, 4):
                if i == j:
                    gpio.output(channel[i], True)
                else:
                    gpio.output(channel[j], False)

    # gpio.cleanup()


def on():
    turn('left')
    turn('rigth')
    turn('rigth')
    turn('left')
