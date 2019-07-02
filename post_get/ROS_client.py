# -*- encoding: utf-8 -*-

# +-----------------------------------------+
# | @File    :   ROS_client.py              |
# | @Time    :   2019/07/01 20:50:15        |
# | @Author  :   Glory Huang                |
# | @Contact :   gloryhry@stu.xjtu.edu.cn   |
# +-----------------------------------------+

# here put the import lib
import requests
import time
from requests import exceptions
import uuid
import subprocess
import ast



# 获取网卡的mac地址生成UUID，但是可能mac会变导致每次运行时UUID变化
# def get_mac_address():
#     mac = uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
#     return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])
# #获取本机mac地址
# mac = get_mac_address()
# print(mac) # 我的电脑mac地址会随机生成，所以生成一次后需要保存进文件，不知道ros上面的会怎么样
# ROS_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, mac)
# print(ROS_uuid)

# 读取主板的UUID作为ros的UUID，但是需要root权限
# cmd = subprocess.Popen('dmidecode -s system-uuid'.split())
# print(cmd)
uuid="04d5cc68-03f9-e411-a26a-480fcfdf611a"

# 定义传输数据格式
data={
    "car_id":"",
    "current_position_x":0.0,
    "current_position_y":0.0,
    "routine":[[0,0],[1,1]],
    "velocity":0,
    "gas":0,
    "pressure_left_front":0,
    "pressure_right_front":0,
    "pressure_left_behind":0,
    "pressure_right_behind":0,
    "camera_status":False,
    "lidar_status":False,
    "ibeo_status":False }
# 写入数据
data["car_id"]=uuid

print(data)

# while True:
#         # ROS连接请求
#         try:
#             # 循环发送ROS的数据信息，设置3s超时    
#             r= requests.post("http://127.0.0.1:5000/ROS",data=data,timeout=3)
#             # r就是接收到的ORDER数据。r.text指把收到的content转为str
#             print("ROS respons:",r.text)
#         except exceptions.Timeout as e:
#             print(str(e))
#         # 如果断线，等待3s后重连    
#         except exceptions.ConnectionError as e:
#             print(str(e))
#             time.sleep(3)
#         time.sleep(1)