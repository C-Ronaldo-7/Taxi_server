#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# @File    :   server.py
# @Time    :   2019/06/24 22:34:56
# @Author  :   Glory Huang
# @Contact :   gloryhry@stu.xjtu.edu.cn

# here put the import lib

# here put the import lib
import socketserver as SocketServer  #导入SocketServer，多线程并发由此类实现
import json
import time

# 有关数据交换的相关变量
# 订单表
# ｛
#   "car_id": int，
#   "person_id"： str，
#   "is_start_nav": bool,				user control
#   "is_arrive_start": bool,				taxi control
#   "is_in_vehicle": bool,				user control
#   "is_reach_target": bool,				taxi(to false)/user(to true) control
#   "start_position": [float, float],			user control
#   "target_position": [float, float],			user control
# ｝
# 车表
# {
#   "current_position": [float, float],			taxi control
#   "routine": [[float,float],...,[float,float]],       taxi control
#   "velocity": float                   taxi control
#   "gas": float                        taxi control
#   "pressure_left_front": float        taxi control
#   "pressure_right_front": float        taxi control
#   "pressure_left_behind": float        taxi control
#   "pressure_right_behind": float        taxi control
#   "camera_status": bool               taxi control
#   "lidar_status": bool                taxi control
#   "ibeo_status": bool                  taxi control
# }
# 客户端表
# {
#   "person_id"： str，
#   "is_start_nav": bool,				user control
#   "is_in_vehicle": bool,				user control
#   "is_reach_target": bool,				taxi(to false)/user(to true) control
#   "start_position": [float, float],			user control
#   "target_position": [float, float],			user control
# }


source_data = {
    "camera_status": "False",
    "current_position": [],
    "gas": 0,
    "ibeo_status": "False",
    "is_arrive_start": "False",
    "is_in_vehicle": "False",
    "is_reach_target": "False",
    "is_start_nav": "False",
    "lidar_status": "False",
    "pressure_left_behind": 0,
    "pressure_left_front": 0,
    "pressure_right_behind": 0,
    "pressure_right_front": 0,
    "routine": [],
    "start_position": [],
    "target_position": [],
    "velocity": 0,
    "time": ""
}

def send_msg(socket,source_data):
    data = json.dumps(source_data)
    data = data + '\n'  # 增加 \n 终止符，用于分割不同次的消息
    data = data.encode()  # 转为byte格式
    if not data: return False
    socket.request.sendall(data)  # 服务器主动推送消息
    print("send to %s msg:%s" % (socket.client_address,source_data))
    return True

class MySockServer(SocketServer.BaseRequestHandler):  #定义一个类
    def handle(self):  #handle(self)方法是必须要定义的，可以看上面的说明
        print('Got a new connection from', self.client_address)
        print(self.request)
        print(self.client_address)
        while True:
            # data = self.request.recv(1024)  #需要通过self的方法调用数据接收函数
            # print(data)
            # if not data:
            #     break
            # datarecv = data.decode()
            # print("recv data from:%s ;data is:%s" %
            #       (self.client_address, datarecv))

            # self.request.send(data.upper())  #需要通过self的方法调用数据接收函数

            msg_time = str(time.strftime("%H:%M:%S"))
            source_data["time"] = msg_time  # 修改json中“time”的值
            if not send_msg(self,source_data):
                break
            time.sleep(1)


if __name__ == '__main__':  #并非一定要用这样的方式，只是建议这样使用
    HOST = ''  #定义侦听本地地址口（多个IP地址情况下），这里表示侦听所有
    PORT = 50008  #Server端开放的服务端口
    s = SocketServer.ThreadingTCPServer((HOST, PORT), MySockServer)
    #调用SocketServer模块的多线程并发函数
    s.serve_forever()  #持续接受客户端的连接
