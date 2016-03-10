import RPi.GPIO as gpio
import time


def turn(direction):
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)

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

    #gpio.cleanup()


def on():
    turn('left')
    turn('rigth')
    turn('rigth')
    turn('left')
