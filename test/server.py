#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# @File    :   server.py
# @Time    :   2019/06/27 20:33:55
# @Author  :   Glory Huang 
# @Contact :   gloryhry@stu.xjtu.edu.cn

# here put the import lib
import socketserver as SocketServer  #导入SocketServer，多线程并发由此类实现
import json
import time
import threading
from multiprocessing import Lock

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
order_data = {
    "car_id": 0,
    "person_id": "0000",
    "is_start_nav": False,
    "is_arrive_start": False,
    "is_in_vehicle": False,
    "is_reach_target": False,
    "start_position": [0, 0],
    "target_position": [1, 1]
}
order_lock = Lock()

car_data = {
    "car_id": 0,
    "current_position": [0, 0],
    "routine": [[0, 0], [1, 1]],
    "velocity": 0.0,
    "gas": 0.0,
    "pressure_left_front": 0.0,
    "pressure_right_front": 0.0,
    "pressure_left_behind": 0.0,
    "pressure_right_behind": 0.0,
    "camera_status": False,
    "lidar_status": False,
    "ibeo_status": False
}
car_lock = Lock()

client_data = {
    "person_id": "0000",
    "is_start_nav": False,
    "is_in_vehicle": False,
    "is_reach_target": False,
    "start_position": [0, 0],
    "target_position": [1, 1]
}
client_lock = Lock()


def send_msg(socket, source_data):
    data = json.dumps(source_data)
    data = data + '\n'  # 增加 \n 终止符，用于分割不同次的消息
    data = data.encode()  # 转为byte格式
    if not data: return False
    socket.request.sendall(data)  # 服务器主动推送消息
    # print("send to %s msg:%s" % (socket.client_address, source_data))
    return True


def get_msg(socket):
    data = socket.request.recv(1024).decode()
    data = data.split('\n')
    get_data = json.loads(data[0])
    return get_data


class send_msg_Server(SocketServer.BaseRequestHandler):  #定义一个类
    def handle(self):  #handle(self)方法是必须要定义的，可以看上面的说明
        print('Got a new connection from', self.client_address)
        print(self.request)
        print(self.client_address)
        while True:
            # TODO: 从car_data数据库读取car_data

            # 给客户端发送car_data信息
            if not send_msg(self, car_data):
                break
            time.sleep(1)


class get_client_data_server(SocketServer.BaseRequestHandler):
    def handle(self):
        print('Got a new connection from', self.client_address)
        #第一次从客户端收到消息
        get_data = get_msg(self)
        #添加互斥锁
        client_lock.acquire()
        #修改client_data的值
        for item in get_data.keys():
            client_data[item] = get_data[item]
        #互斥锁释放
        client_lock.release()
        # TODO: 跟新client_data数据库信息

        # 系统安排车辆
        # TODO: 从car数据库中找到空闲的车辆。给订单分配车辆

        #更新order_data表单
        #互斥锁
        order_lock.acquire()
        order_data["car_id"] = car_data["car_id"]
        for item in get_data.keys():
            if get_data[item] != order_data[item]:
                order_data[item] = get_data[item]
        #互斥锁释放
        order_lock.release()
        # TODO: 跟新order数据库信息

        while True:
            get_data = get_msg(self)  #从客户端获取client_data
            #添加互斥锁
            client_lock.acquire()
            #修改client_data的值
            for item in get_data.keys():
                client_data[item] = get_data[item]
            #互斥锁释放
            client_lock.release()
            # TODO: 跟新client_data数据库信息

            #更新order_data表单
            #互斥锁
            order_lock.acquire()
            for item in get_data.keys():
                if get_data[item] != order_data[item]:
                    order_data[item] = get_data[item]
            #互斥锁释放
            order_lock.release()
            # TODO: 跟新order数据库信息

            print(client_data)


# TODO: 从数据库中跟新car_data表单
def update_car_data():
    pass


def get_client(HOST, PORT):
    s = SocketServer.ThreadingTCPServer((HOST, PORT), get_client_data_server)
    s.serve_forever()


def send_client(HOST, PORT):
    s = SocketServer.ThreadingTCPServer((HOST, PORT), send_msg_Server)
    s.serve_forever()


if __name__ == '__main__':  #并非一定要用这样的方式，只是建议这样使用
    HOST = ''  #定义侦听本地地址口（多个IP地址情况下），这里表示侦听所有
    PORT = 50008  #Server端开放的服务端口

    # 由于s.server_forever()会循环执行，所以放入单独一个线程进行循环
    # 服务器接受数据端口 50009
    get = threading.Thread(target=get_client, args=(HOST, 50009))
    # 服务器发送数据端口 50008
    send = threading.Thread(target=send_client, args=(HOST, 50008))
    get.start()
    send.start()