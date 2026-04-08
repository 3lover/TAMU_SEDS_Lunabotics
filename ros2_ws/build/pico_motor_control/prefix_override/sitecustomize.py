import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/lunabotics/lunabotics/ros2_ws/install/pico_motor_control'
