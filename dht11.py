import RPi.GPIO as gpio
import time


def startSignal(channel):
    # 发送开始信号

    gpio.setup(channel, gpio.OUT)
    gpio.output(channel, gpio.LOW)
    time.sleep(0.2)
    gpio.output(channel, gpio.HIGH)


def getData(channel):
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
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
        #print ("当前温度为%d,相对湿度为%d" % (temperature,humidity))
        return (u"当前温度为%d℃,相对湿度为%d%%") % (temperature,humidity)
    else:
        return getData(channel)
    #gpio.cleanup()


def get_temperature():
    channel = 4
    return getData(channel)
