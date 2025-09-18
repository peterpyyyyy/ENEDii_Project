#!/usr/bin/env python3
from robot_code import dual_sensor_follow_line, arm_initialize,single_sensor_follow_line

arm_initialize()

single_sensor_follow_line(
    kp=0.1411,
    ki=0.00,
    kd=0.32, 
    target=45, 
    speed=45.5,
    side='left'
)