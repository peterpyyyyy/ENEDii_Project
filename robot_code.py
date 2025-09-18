"""主体函数,不要调用除了dual_sensor_follow_line和single_sensor_follow_line以外的函数,因为相关函数已经集成在里面"""

#!/usr/bin/env micropython
from time import sleep
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, MoveTank, Motor
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
#from ev3dev2.display import 

#实例化对象
tank = MoveTank(OUTPUT_A, OUTPUT_B)
csL = ColorSensor(INPUT_1)
csR = ColorSensor(INPUT_2)
ifcs = UltrasonicSensor(INPUT_3)
armMotor = Motor(OUTPUT_C)

# 添加一个全局变量，用于标记是否刚刚执行过 pick_up_trash
just_picked_up = False
just_dropped = False
intergral = 0  # 初始化 PID 的积分项

#输出限制，确保输出在-100到100之间
def output_limit(rawOutput):
    cookedOutput = max(min(rawOutput,100),-100)
    return cookedOutput

#颜色检测，参数可选左右传感器（left/right）、目标颜色，返回True/False
def colour_detection(color, side):
    'color example: Red Blue Black etc'
    if side == "left":
        if csL.color_name == color:
            return True
        
    else:
        if csR.color_name == color:
            return True
    return False

#超声波测距，检测前方是否有障碍物，默认距离15cm，返回True/False
def object_detection(distance = 15):
    if ifcs.distance_centimeters < distance:
        return True
    else:
        return False

#在双传感器循迹中调用，判断是否可以继续前进
def can_we_move_duo():
    global just_picked_up
    global just_dropped  # 使用全局变量
    if just_dropped:
        #colour_detection(color='Black', side='right')
        return True
    elif just_picked_up: # 如果刚刚捡起垃圾
        if  colour_detection(color='Red', side='right')==True: #用于放下垃圾的颜色检测
            tank.off()
            put_down_trash()
            just_dropped = True
            #go_around()
        return True
    elif object_detection():  # 如果检测到障碍物
        pick_up_trash()
        just_picked_up = True  # 标记刚刚执行过 pick_up_trash
        sleep(0.2)
        return True
    elif colour_detection(color='Blue', side='right')==True:   #用于终止在指定颜色 
        tank.off()
        return False
    return True

#在单传感器循迹中调用，判断是否可以继续前进
def can_we_move_single():
    global just_picked_up  # 使用全局变量
    global just_dropped 
    if just_dropped: # 如果刚刚放下垃圾
        return True
    elif just_picked_up: # 如果刚刚捡起垃圾
        if  colour_detection(color='Red', side='right')==True: #用于放下垃圾的颜色检测
            tank.off()
            put_down_trash()
            just_dropped = True
            #go_around()
            return True
    elif object_detection(distance=18):  # 如果未捡起垃圾
        pick_up_trash(wait_second=0.3)
        just_picked_up = True  # 标记刚刚执行过 pick_up_trash
        sleep(0.2)
        return True
    return True


#双传感器循迹，参数：kp, ki, kd, 左右传感器目标值targetL/targetR，白色阈值white，速度speed
def dual_sensor_follow_line(kp, ki, kd, targetL, targetR, white, speed):
    
    intergral = 0
    last_erro = 0
    erroL = 0
    erroR = 0
    turn = 0
    
    while can_we_move_duo():
        # Calculate the deviation from the target light intensity
        erroL = max(targetL - csL.reflected_light_intensity,0)#左侧踩线时erroL为正
        erroR = max(targetR - csR.reflected_light_intensity,0)#右侧踩线时erroR为正
        # Calculate the turn value
        total_erro = erroL - erroR#左边踩线时total_erro为正，右边踩线时total_erro为负
        intergral = intergral + total_erro
        derivative = total_erro - last_erro#接近目标值时，derivative为负
        turn = kp * total_erro + ki * intergral + kd * derivative
        last_erro = total_erro

        # Set the turn value as the tank's turn value
        tank.on(left_speed=((output_limit(speed - turn))+4), right_speed=output_limit(speed + turn))
        # Sleep for the specified time
        sleep(0.002)

#单传感器循迹，参数：kp, ki, kd, 传感器目标值target，速度speed，传感器side（left/right）
def single_sensor_follow_line(kp, ki, kd, target, side, speed):

    intergral = 0
    last_erro = 0
    error = 0
    turn = 0

    if side == 'left':
        sensor = csL
    elif side == 'right':
        sensor = csR

    while can_we_move_single():

        error = target - sensor.reflected_light_intensity
        intergral = intergral + error
        derivative = error - last_erro
        turn = kp * error + ki * intergral + kd * derivative
        last_erro = error

        if side == 'right':
            turn *= -1

        tank.on(left_speed=output_limit(speed - turn), right_speed=output_limit(speed + turn))
        sleep(0.002)

#绕过障碍物
def go_around():
    tank.on_for_rotations(left_speed = -10, right_speed= -10, rotations=0.57, brake=True)
    tank.on_for_rotations(left_speed = 40, right_speed= 15, rotations=1.1, brake=False)
    tank.on_for_rotations(left_speed = 30, right_speed= 50, rotations=2.5, brake=False)
    while csL.reflected_light_intensity > 60:
        tank.on(left_speed=20, right_speed=6)

#arm初始化
def arm_initialize():
    #armMotor.on_to_position(speed=50, position=-20, brake=True)
    armMotor.on_for_seconds(speed=100, seconds=1,brake=True)

#拾取垃圾
def pick_up_trash(wait_second=0.6):
    global intergral  # 声明使用全局变量
    # 执行拾取垃圾的操作
    armMotor.on_for_seconds(speed=100, seconds=0.5, brake=True)
    tank.on_for_seconds(left_speed=15, right_speed=15, seconds=wait_second)
    armMotor.on_for_seconds(speed=-80, seconds=0.5, brake=True)
    
    # 重置 PID 的积分项
    intergral = 0

#放下垃圾
def put_down_trash():
    tank.on_for_seconds(left_speed=15, right_speed=-15, seconds=0.70)
    tank.on_for_seconds(left_speed=15, right_speed=15, seconds=0.70)
    armMotor.on_for_seconds(speed=100, seconds=1,brake=True)
    tank.on_for_seconds(left_speed=-15, right_speed=-15, seconds=0.70)
    tank.on_for_seconds(left_speed=-15, right_speed=15, seconds=0.70)
    #sleep(0.05)

