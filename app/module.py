import time
import RPi.GPIO as gpio

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

class ModuleHumiture:

    def __init__(self, channel):
        self.channel = channel

    def startsignal(self):
        # 发送开始信号
        gpio.setup(self.channel, gpio.OUT)
        gpio.output(self.channel, gpio.LOW)
        time.sleep(0.2)
        gpio.output(self.channel, gpio.HIGH)

    def getdata(self):
        time.sleep(1)
        data = []
        j = 0

        self.startsignal()
        time.sleep(0.5)
        self.startsignal()

        # 等待dht11回应
        gpio.setup(self.channel, gpio.IN)

        while gpio.input(self.channel) == gpio.LOW:
            continue

        while gpio.input(self.channel) == gpio.HIGH:
            continue

        while j < 40:
            k = 0
            j += 1
            while gpio.input(self.channel) == gpio.LOW:
                continue

            while gpio.input(self.channel) == gpio.HIGH:
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
            return (u"当前温度为%d℃,相对湿度为%d%%") % (temperature, humidity)
        else:
            return self.getdata()

    def get_humiture(self):
        # channel = 4
        return self.getdata()


class ModuleHumanInfraredInduction:

    def __init__(self, channel):
        self.channel = channel
        gpio.setup(self.channel, gpio.IN)

    def has_people(self):
        # channel = 27
        # time.sleep(60)
        # gpio.setup(channel,gpio.OUT)
        # gpio.output(channel,gpio.HIGH)
        if gpio.input(self.channel):
            return 1
        else:
            return 0


class StepperMotor:

    def __init__(self, channel):
        self.channel = channel


    def turn(self, direction):

        # channel = [13, 19, 16, 20]

        arr = [0, 1, 2, 3]

        if direction == 'left':
            arr = [3, 2, 1, 0]

        for i in self.channel:
            gpio.setup(i, gpio.OUT)
            gpio.output(i, False)

        # 64   angle= 45
        for x in range(0, 64):
            for i in arr:
                time.sleep(0.01)
                for j in range(0, 4):
                    if i == j:
                        gpio.output(self.channel[i], True)
                    else:
                        gpio.output(self.channel[j], False)

    def auto_turn(self):
        self.turn('left')
        self.turn('rigth')
        self.turn('rigth')
        self.turn('left')


class Car:

    def __init__(self, channel, pin1, pin2, speed=10, frequency=1):
        self.channel = channel
        self.pin1 = pin1
        self.pin2 = pin2
        self.speed = speed
        self.frequency = frequency
        self.p1 = None
        self.p2 = None
        print('creat car')

        self.init_car()

    def init_car(self):
        for i in self.channel:
            gpio.setup(i, gpio.OUT)

        gpio.setup(self.pin1, gpio.OUT)
        gpio.setup(self.pin2, gpio.OUT)

        self.p1 = gpio.PWM(self.pin1, self.frequency)
        self.p2 = gpio.PWM(self.pin2, self.frequency)

        self.p1.start(self.speed)
        self.p2.start(self.speed)

    def speedplus(self):
        print('enter speedplus')
        print(self.speed)
        self.speed += 10
        if self.speed > 100:
            self.speed = 100
        print(self.speed)
        self.p1.ChangeDutyCycle(self.speed)
        self.p2.ChangeDutyCycle(self.speed)
        print('exit speedplus')

    def speedreduce(self):
        print('enter speedreduce')
        print(self.speed)
        self.speed -= 10
        if self.speed < 10:
            self.speed = 10
        print(self.speed)
        self.p1.ChangeDutyCycle(self.speed)
        self.p2.ChangeDutyCycle(self.speed)
        print('exit speedreduce')

    def up(self):
        print(self.speed)
        gpio.output(self.channel[0], gpio.HIGH)
        gpio.output(self.channel[2], gpio.HIGH)
        gpio.output(self.channel[1], gpio.LOW)
        gpio.output(self.channel[3], gpio.LOW)

    def down(self):
        print(self.speed)
        gpio.output(self.channel[1], gpio.HIGH)
        gpio.output(self.channel[3], gpio.HIGH)
        gpio.output(self.channel[0], gpio.LOW)
        gpio.output(self.channel[2], gpio.LOW)

    def right(self):
        print(self.speed)
        gpio.output(self.channel[3], gpio.LOW)
        gpio.output(self.channel[2], gpio.LOW)
        gpio.output(self.channel[1], gpio.LOW)
        gpio.output(self.channel[0], gpio.HIGH)
        time.sleep(0.5)
        self.stop()

    def left(self):
        print(self.speed)
        gpio.output(self.channel[1], gpio.LOW)
        gpio.output(self.channel[0], gpio.LOW)
        gpio.output(self.channel[3], gpio.LOW)
        gpio.output(self.channel[2], gpio.HIGH)
        time.sleep(0.5)
        self.stop()

    def stop(self):
        for i in self.channel:
            gpio.output(i, gpio.LOW)

