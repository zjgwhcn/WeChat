import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

gpio.setup(26,gpio.OUT,initial=gpio.LOW)
gpio.setup(12,gpio.IN)

def check():
    gpio.output(26,gpio.HIGH)
    time.sleep(0.000015)
    gpio.output(26,gpio.LOW)
    while True:
        if gpio.input(12):
            t1 = time.time()
            break
    while True:
        if not gpio.input(12):
            t2 = time.time()
            break
    print((t2-t1)*340/2)
