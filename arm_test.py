#!/usr/bin/env python3
from robot_code import pick_up_trash, arm_initialize, object_detection, armMotor
from time import sleep
arm_initialize()
while True:
    if object_detection(distance=15):
        pick_up_trash()
        armMotor.brake()
        break