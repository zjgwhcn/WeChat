from flask.ext.script import Manager, Shell
from app import creat_app
import os

app = creat_app(os.environ.get('FLASK_CONFIG') or 'default')
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
