#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# @File    :   client.py
# @Time    :   2019/06/24 22:03:09
# @Author  :   Glory Huang
# @Contact :   gloryhry@stu.xjtu.edu.cn

# here put the import lib
import socket
import time
import json

def doConnect(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except:
        pass
    return sock


def receive_from_server(sockLocal):
    data_rev = sockLocal.recv(1024).decode()  # 从缓存区中读取并转为str格式
    data_rev = data_rev.split('\n')  # 以\n为终止符，分割出最后收到的一次消息
    data_get = data_rev[0]
    # print(type(data_get))
    # print(data_get)
    data = json.loads(data_get)  # 转换为json格式
    return data


def main():
    host, port = "47.96.114.206", 50008
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

if __name__ == "__main__":
    main()