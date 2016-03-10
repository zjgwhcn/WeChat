import RPi.GPIO as gpio


def check():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
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
