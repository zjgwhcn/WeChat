import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

gpio.setup(21,gpio.OUT)
p = gpio.PWM(21,50)
p.start(0)
time.sleep(2)

def right():
    p.ChangeDutyCycle(2.5)
    time.sleep(0.1 )
    p.ChangeDutyCycle(0)
    time.sleep(0.2)

def left():
    p.ChangeDutyCycle(12.5)
    time.sleep(0.1)
    p.ChangeDutyCycle(0)
    time.sleep(0.2)

def turn():
    right()
    time.sleep(0.2)
    left()
    time.sleep(0.2)
    left()
    time.sleep(0.2)
    right()
    time.sleep(0.2)
