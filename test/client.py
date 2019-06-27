#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# @File    :   client.py
# @Time    :   2019/06/27 16:17:38
# @Author  :   Glory Huang
# @Contact :   gloryhry@stu.xjtu.edu.cn

# here put the import lib
import socket
import time
import json
import threading

client_data = {
    "person_id": "0000",
    "is_start_nav": False,
    "is_in_vehicle": False,
    "is_reach_target": False,
    "start_position": [0, 0],
    "target_position": [1, 1]
}


def doConnect(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except:
        pass
    return sock


def send_msg(socket, source_data):
    data = json.dumps(source_data)
    data = data + '\n'  # 增加 \n 终止符，用于分割不同次的消息
    data = data.encode()  # 转为byte格式
    if not data: return False
    socket.sendall(data)  # 服务器主动推送消息
    print("send msg:%s" % (source_data))
    return True


def receive_from_server(sockLocal):
    data_rev = sockLocal.recv(1024).decode()  # 从缓存区中读取并转为str格式
    data_rev = data_rev.split('\n')  # 以\n为终止符，分割出最后收到的一次消息
    data_get = data_rev[0]
    # print(type(data_get))
    # print(data_get)
    data = json.loads(data_get)  # 转换为json格式
    return data


def get_data_client():
    host, port = "192.168.3.18", 50008
    print(host, port)
    sockLocal = doConnect(host, port)

    while True:
        try:
            # 客户端发送消息并接受服务器的返回值
            # msg = str(time.strftime("%H:%M:%S"))
            # msgencode=msg.encode()
            # sockLocal.sendall(msgencode)
            # print ("send msg ok : ",msg)
            # print ("recv data :",sockLocal.recv(1024).decode())

            # 服务器主动推送消息
            data = receive_from_server(sockLocal)
            # print(type(data))
            print(data)

        except socket.error:
            print("ocket error,do reconnect ")
            time.sleep(3)
            sockLocal = doConnect(host, port)
        except:
            print('other error occur ')
            time.sleep(3)
        # time.sleep(1)
    sockLocal.shutdown(2)
    sockLocal.close()


def send_data_client():
    host, port = "192.168.3.18", 50009
    sockLocal = doConnect(host, port)
    while True:
        id = client_data["person_id"]
        id = int(id)
        id = id + 1
        client_data["person_id"] = str(id)
        send_msg(sockLocal, client_data)
        time.sleep(1)


if __name__ == "__main__":
    get = threading.Thread(target=get_data_client)
    send = threading.Thread(target=send_data_client)
    get.start()
    send.start()
