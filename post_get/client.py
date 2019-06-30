# -*- encoding: utf-8 -*-

# +-----------------------------------------+
# | @File    :   client.py                |
# | @Time    :   2019/06/30 21:54:50        |
# | @Author  :   Glory Huang                |
# | @Contact :   gloryhry@stu.xjtu.edu.cn   |
# +-----------------------------------------+

# here put the import lib
import requests

client_data={
  "person_id":1,
  "is_start_nav": True,
  "is_in_vehicle": True,
  "is_reach_target": False,
  "start_position_x": 0.2,
  "start_position_y": 0.2,
  "target_position_x": 1.9,
  "target_position_y": 1.9
}
car_data = {
    "car_id": 1,
    "current_position_x": 0,
    "current_position_y": 5,
    "routine": [[0, 1], [2, 6], [1, 5]],
    "velocity": 1.2,
    "gas": 0.2,
    "pressure_left_front": 0.2,
    "pressure_left_behind": 1.9,
    "pressure_right_front": 1.9,
    "pressure_right_behind": 4.6,
    "camera_status": False,
    "lidar_status": False,
    "ibeo_status": False
}
r = requests.post("http://127.0.0.1:5000/ROS", data=car_data)
print("ROS respons:",r.text)
r= requests.post("http://127.0.0.1:5000/client",data=client_data)
print("client respons:",r.text)