import RPi.GPIO as gpio
import time
import pygame
from threading import Thread

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(21,gpio.IN)

count = 0
flag = 1

def countspeed():
    #print('enter countspeed')
    global flag,count
    while flag:
        #print('enter loop')
        if gpio.input(21) != gpio.input(21):
            count += 1
            #print('count+1')
    #print('exit countspeeds')
    
def print_count():
    global count
    print(count,end = ',')
    count = 0

def sleep():
    #print('enter sleep')
    while True:
        t = Thread(target = countspeed)
        t.setDaemon(True)
        t.start()
        #print('begin sleep')
        time.sleep(1)
        #print('exit sleep')
        global flag
        flag = 0
        print_count()
        flag = 1

class Car:

    def __init__(self, channel=[24,25,5,6], pin1=22, pin2=23, speed=10, frequency=8):
        self.channel = channel
        self.pin1 = pin1
        self.pin2 = pin2
        self.speed = speed
        self.frequency = frequency
        self.p1 = None
        self.p2 = None
        self.flag = 0
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

    def frequencyplus(self):
        self.stop()
        self.frequency += 1
        print(self.frequency)
        self.p1.ChangeFrequency(self.frequency)
        self.p2.ChangeFrequency(self.frequency)
        if self.flag:
            pass
            #self.down()
        else:
            pass
            #self.up()

    def frequencyreduce(self):
        self.stop()
        self.frequency -= 1
        if self.frequency <= 0:
            self.frequency = 1
        print(self.frequency)
        self.p1.ChangeFrequency(self.frequency)
        self.p2.ChangeFrequency(self.frequency)
        if self.flag:
            pass
            self.down()
        else:
            pass
            #self.up()

    def speedplus(self):
        self.stop()
        self.speed += 10
        if self.speed > 100:
            self.speed = 100
        print('\n',self.speed)
        self.p1.ChangeDutyCycle(self.speed)
        self.p2.ChangeDutyCycle(self.speed)
        if self.flag:
            pass
            #self.down()
        else:
            pass
            #self.up()

    def speedreduce(self):
        self.stop()
        self.speed -= 10
        if self.speed < 10:
            self.speed = 10
        print('\n',self.speed)
        self.p1.ChangeDutyCycle(self.speed)
        self.p2.ChangeDutyCycle(self.speed)
        if self.flag:
            pass
            #self.down()
        else:
            pass
            #self.up()

    def up(self):
        #print('up')
        self.flag = 0
        gpio.output(self.channel[0], gpio.HIGH)
        gpio.output(self.channel[2], gpio.HIGH)
        gpio.output(self.channel[1], gpio.LOW)
        gpio.output(self.channel[3], gpio.LOW)
        t = Thread(target = countspeed)
        t.setDaemon(True)
        t.start()
        time.sleep(1)
        self.stop()
        #print('exit sleep')
        global flag
        flag = 0
        print_count()
        flag = 1

    def down(self):
        #print('down')
        self.flag = 1
        gpio.output(self.channel[1], gpio.HIGH)
        gpio.output(self.channel[3], gpio.HIGH)
        gpio.output(self.channel[0], gpio.LOW)
        gpio.output(self.channel[2], gpio.LOW)

    def right(self):
        #print('right')
        gpio.output(self.channel[3], gpio.LOW)
        gpio.output(self.channel[2], gpio.LOW)
        gpio.output(self.channel[1], gpio.LOW)
        gpio.output(self.channel[0], gpio.HIGH)
        time.sleep(1)
        self.stop()
        #print('exit right')

    def left(self):
        print('left')
        gpio.output(self.channel[1], gpio.LOW)
        gpio.output(self.channel[0], gpio.LOW)
        gpio.output(self.channel[3], gpio.LOW)
        gpio.output(self.channel[2], gpio.HIGH)
        time.sleep(1)
        self.stop()

    def stop(self):
        #print('stop')
        for i in self.channel:
            gpio.output(i, gpio.LOW)

pygame.init()
screen=pygame.display.set_mode([640,480])
screen.fill([255,255,255])
upimage = pygame.image.load('/root/WeChat/app/static/up.png')
downimage = pygame.image.load('/root/WeChat/app/static/down.png')
leftimage = pygame.image.load('/root/WeChat/app/static/left.png')
rightimage = pygame.image.load('/root/WeChat/app/static/right.png')
plusimage = pygame.image.load('/root/WeChat/app/static/plus.png')
reduceimage = pygame.image.load('/root/WeChat/app/static/reduce.png')
plusimage2 = pygame.image.load('/root/WeChat/app/static/plus.png')
reduceimage2 = pygame.image.load('/root/WeChat/app/static/reduce.png')
stopimage = pygame.image.load('/root/WeChat/app/static/dark.png')
screen.blit(upimage,[140,200])
screen.blit(downimage,[140,280])
screen.blit(leftimage,[100,240])
screen.blit(rightimage,[180,240])
screen.blit(plusimage,[440,200])
screen.blit(reduceimage,[480,200])
screen.blit(stopimage,[440,240])
screen.blit(plusimage2,[440,280])
screen.blit(reduceimage2,[480,280])
pygame.display.flip()
car = Car()
#t2 = Thread(target = sleep)
#t2.setDaemon(True)
#t2.start()
while True:
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN and 140<=event.pos[0]<=180 \
           and 200<=event.pos[1]<=240:
            car.up()

        elif event.type==pygame.MOUSEBUTTONDOWN and 140<=event.pos[0]<=180 \
           and 280<=event.pos[1]<=320:
            car.down()

        elif event.type==pygame.MOUSEBUTTONDOWN and 100<=event.pos[0]<=140 \
           and 240<=event.pos[1]<=280:
            car.left()

        elif event.type==pygame.MOUSEBUTTONDOWN and 180<=event.pos[0]<=220 \
           and 240<=event.pos[1]<=280:
            car.right()

        elif event.type==pygame.MOUSEBUTTONDOWN and 440<=event.pos[0]<=480 \
           and 200<=event.pos[1]<=240:
            car.speedplus()

        elif event.type==pygame.MOUSEBUTTONDOWN and 480<=event.pos[0]<=520 \
           and 200<=event.pos[1]<=240:
            car.speedreduce()

        elif event.type==pygame.MOUSEBUTTONDOWN and 440<=event.pos[0]<=480 \
           and 280<=event.pos[1]<=320:
            car.frequencyplus()

        elif event.type==pygame.MOUSEBUTTONDOWN and 480<=event.pos[0]<=520 \
           and 280<=event.pos[1]<=320:
            car.frequencyreduce()

        elif event.type==pygame.MOUSEBUTTONDOWN and 440<=event.pos[0]<=480 \
           and 240<=event.pos[1]<=280:
            car.stop()



