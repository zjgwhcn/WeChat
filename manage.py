from flask.ext.script import Manager, Shell
from app import creat_app
import os
import RPi.GPIO as gpio

app = creat_app(os.environ.get('FLASK_CONFIG') or 'default')
manager = Manager(app)

if __name__ == '__main__':
    try:
        manager.run()
    except KeyboardInterrupt:
        print('重置GPIO')
        gpio.cleanup()
