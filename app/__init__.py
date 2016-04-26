from flask import Flask
from config import config
from .module import Car,ModuleHumiture,ModuleHumanInfraredInduction,StepperMotor

# car = Car([24, 25, 5, 6], 22, 23)
motor = StepperMotor([13,19,16,20])
humiture = ModuleHumiture(4)
humaninfrared = ModuleHumanInfraredInduction(27)


def creat_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
