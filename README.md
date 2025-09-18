# CQU UC学院 ENEDII EV3 Project

本项目基于 LEGO EV3 机器人，使用 Python（ev3dev2 库）实现了双/单传感器循迹、垃圾拾取与放置、传感器校准等功能。

## 目录结构

```
final code/
├── robot_code.py         # 主体功能代码，包含循迹、垃圾处理等核心逻辑
├── just_follow_line.py   # 仅双传感器循迹主程序入口
├── straight.py           # 单传感器循迹主程序入口
├── calibrate.py          # 颜色传感器校准与显示工具
```

## 快速开始

1. **硬件连接**
   - 左颜色传感器：EV3 INPUT_1
   - 右颜色传感器：EV3 INPUT_2
   - 超声波传感器：EV3 INPUT_3
   - 左/右驱动电机：EV3 OUTPUT_A / OUTPUT_B
   - 机械臂电机：EV3 OUTPUT_C

2. **运行循迹主程序**
   - 双传感器循迹：
     ```bash
     python3 just_follow_line.py
     ```
   - 单传感器循迹：
     ```bash
     python3 straight.py
     ```

3. **传感器校准与调试**
   - 显示当前左右颜色传感器光强值：
     ```bash
     python3 calibrate.py
     ```

## 主要功能说明

- **robot_code.py**
  - `dual_sensor_follow_line`：双传感器 PID 循迹，支持障碍物检测与垃圾处理。
  - `single_sensor_follow_line`：单传感器 PID 循迹。
  - `pick_up_trash` / `put_down_trash`：垃圾拾取与放置动作。
  - `object_detection`：超声波障碍物检测。
  - `colour_detection`：颜色检测辅助决策。
  - `arm_initialize`：机械臂初始化。

- **just_follow_line.py**
  - 仅调用双传感器循迹主流程，适合基础循迹测试。

- **straight.py**
  - 单传感器循迹主流程，适合直线或简单路径测试。

- **calibrate.py**
  - 实时显示左右颜色传感器光强值，便于调试与阈值设定。

## 参数调整建议

- `kp`, `ki`, `kd`：PID 控制参数，需根据实际场地和机器人调整。
- `targetL`, `targetR`：循迹目标光强值，建议通过 `calibrate.py` 获取。
- `white`：白色阈值，用于区分赛道与背景。
- `speed`：循迹速度，建议根据场地和任务灵活调整。

## 注意事项

- 请确保所有传感器和电机已正确连接并初始化。
- 运行前建议使用 `calibrate.py` 校准传感器，获取合适的光强阈值。
- 若机器人无反应或报错，请检查硬件连接、电池电量及端口设置。

## 参考

- [ev3dev2 官方文档](https://python-ev3dev.readthedocs.io/en/latest/)
- LEGO EV3 教学资料

---

如有问题或建议，欢迎提交 Issue 或 Pull Request！
