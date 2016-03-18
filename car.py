import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

INT1 = 24
INT2 = 25
INT3 = 5
INT4 = 6

INT = [INT1, INT2, INT3, INT4]
for i in INT:
    gpio.setup(i, gpio.OUT)

pin1,pin2 = 22,23
gpio.setup(pin1,gpio.OUT)
gpio.setup(pin2,gpio.OUT)

p1 = gpio.PWM(pin1,8)
p2 = gpio.PWM(pin2,8)
speed = 10

def addspeed():
    global speed
    speed += 10
    if speed > 100:
        speed = 100
    p1.ChangeDutyCycle(speed)
    p2.ChangeDutyCycle(speed)    

def downspeed():
    global speed
    speed -= 10
    if speed < 30:
        speed = 30
    p1.ChangeDutyCycle(speed)
    p2.ChangeDutyCycle(speed)
    
def up():
    p1.start(40)
    p2.start(40)
    gpio.output(INT1, gpio.HIGH)
    gpio.output(INT3, gpio.HIGH)
    gpio.output(INT2, gpio.LOW)
    gpio.output(INT4, gpio.LOW)
    #time.sleep(1)
    #stop()


def down():
    p1.start(40)
    p2.start(40)
    gpio.output(INT2, gpio.HIGH)
    gpio.output(INT1, gpio.LOW)
    gpio.output(INT4, gpio.HIGH)
    gpio.output(INT3, gpio.LOW)
    #time.sleep(1)
    #stop()


def right():
    p1.start(10)
    gpio.output(INT4, gpio.LOW)
    gpio.output(INT3, gpio.LOW)
    gpio.output(INT2, gpio.LOW)
    gpio.output(INT1, gpio.HIGH)
    time.sleep(0.5)
    stop()


def left():
    p2.start(10)
    gpio.output(INT2, gpio.LOW)
    gpio.output(INT1, gpio.LOW)
    gpio.output(INT4, gpio.LOW)
    gpio.output(INT3, gpio.HIGH)
    time.sleep(0.5)
    stop()


def stop():
    for i in INT:
        gpio.output(i, gpio.LOW)
