#!/usr/bin/env python3
from robot_code import dual_sensor_follow_line, arm_initialize

arm_initialize()

dual_sensor_follow_line(
    kp=0.1401,
    ki=0.00,
    kd=0.36, 
    targetL=100, 
    targetR=100,
    white=74,
    speed=10.5)