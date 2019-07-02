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
import json

# 以下两种获取UUID的方法选其中一个

# 方法一： 获取网卡的mac地址生成UUID，但是可能mac会变导致每次运行时UUID变化
# def get_mac_address():
#     mac = uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
#     return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])
# #获取本机mac地址
# mac = get_mac_address()
# print(mac) # 我的电脑mac地址会随机生成，所以生成一次后需要保存进文件，不知道ros上面的会怎么样
# ROS_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, mac)
# print(ROS_uuid)

# 方法二： 读取主板的UUID作为ros的UUID，但是需要root权限
# cmd = subprocess.Popen('dmidecode -s system-uuid'.split())
# print(cmd)

# 默认已经获取到uuid
uuid = "04d5cc68-03f9-e411-a26a-480fcfdf611a"

# 定义传输数据格式，可能后续还要改变此格式
data = {
    "car_id": "",
    "current_position_x": 0.0,
    "current_position_y": 0.0,
    "routine": "[[0,0],[1,1]]",
    "velocity": 0,
    "gas": 0,
    "pressure_left_front": 0,
    "pressure_right_front": 0,
    "pressure_left_behind": 0,
    "pressure_right_behind": 0,
    "camera_status": True,
    "lidar_status": True,
    "ibeo_status": True
}
# 写入数据
data["car_id"] = uuid
# print(data)

# # 注册车辆进数据库
# # 平时通信的时候可以不运行
# try:
#     # 与服务器通信时必须用json格式的数据
#     response = requests.post("http://127.0.0.1:5000/ROS/register",
#                              data=json.dumps(data),
#                              timeout=3)
#     print(response.text)
# except requests.exceptions.RequestException as e:  #
#     print(str(e))

while True:
    # ROS连接请求
    try:
        # 循环发送ROS的数据信息，设置3s超时
        # 与服务器通信时必须用json格式的数据
        r = requests.post("http://127.0.0.1:5000/ROS",
                          data=json.dumps(data),
                          timeout=3)
        # r就是接收到的ORDER数据。
        if r.text == "数据库中没有此车信息，请注册":
            print("ROS respons:", r.text)
            break

        # r.text指把收到的content转为str
        print("ROS respons:", r.text)
        # str转为dict的数据格式
        order_data = json.loads(r.text)
        # 后面可以使用order_data数据，do what you want to do.

        

    except exceptions.Timeout as e:
        print(str(e))
    # 如果断线，等待3s后重连
    except exceptions.ConnectionError as e:
        print(str(e))
        time.sleep(3)
    time.sleep(1)
