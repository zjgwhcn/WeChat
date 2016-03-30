from flask import Blueprint
from ..module import Car,ModuleHumiture,ModuleHumanInfraredInduction,StepperMotor

main = Blueprint('main', __name__)
car = Car([24, 25, 5, 6], 22, 23)
motor = StepperMotor([13,19,16,20])
humiture = ModuleHumiture(4)
humaninfrared = ModuleHumanInfraredInduction(27)

from . import views