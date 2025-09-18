#!/usr/bin/env python3
from ev3dev2.display import Display
from textwrap import wrap
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import ColorSensor
from time import sleep

lcd = Display()
csL = ColorSensor(INPUT_1)
csR = ColorSensor(INPUT_2)


def show_text(font_name='courB24', font_width=15, font_height=24):
    while True:
        try:
            lcd.clear()
            # 动态获取传感器的光强值
            left_intensity = csL.reflected_light_intensity if csL.reflected_light_intensity is not None else 0
            right_intensity = csR.reflected_light_intensity if csR.reflected_light_intensity is not None else 0
            text = "R:{1},L:{0}".format(left_intensity, right_intensity)
            
            # 自动换行并显示
            wrapped_text = wrap(text, width=int(180 / font_width))
            for i in range(len(wrapped_text)):
                x_val = 89 - font_width / 2 * len(wrapped_text[i])
                y_val = 63 - (font_height + 1) * (len(wrapped_text) / 2 - i)
                lcd.text_pixels(wrapped_text[i], False, x_val, y_val, font=font_name)
            lcd.update()
            sleep(0.1)  # 添加短暂延迟
        except Exception as e:
            print("Error: {}".format(e))
            lcd.clear()
            lcd.text_pixels("Error", False, 50, 50, font=font_name)
            lcd.update()

show_text()