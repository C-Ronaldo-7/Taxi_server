# -*- encoding: utf-8 -*-

# +-----------------------------------------+
# | @File    :   client.py                |
# | @Time    :   2019/07/01 15:04:36        |
# | @Author  :   Glory Huang                |
# | @Contact :   gloryhry@stu.xjtu.edu.cn   |
# +-----------------------------------------+

# here put the import lib
import requests
import time
from requests import exceptions
import hashlib
from requests.adapters import HTTPAdapter

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

# 生成MD5
def genearteMD5(str):
    # 创建md5对象
    hl = hashlib.md5()
    # Tips
    # 此处必须声明encode
    # 否则报错为：hl.update(str) Unicode-objects must be encoded before hashing
    hl.update(str.encode(encoding='utf-8'))
    return hl.hexdigest()


# 输入账号密码和 登录or新建账号
account = "17691053351"
password = genearteMD5("0013")
login_or_create = True
# 传送的dict数据
client = dict(account=account,
              password=password,
              login_or_create=login_or_create)
# 与服务器通信，校验账号或者新建账号
print(time.strftime('%Y-%m-%d %H:%M:%S'))
try:
    response = requests.post("http://127.0.0.1:5000/client/login",
                             data=client,
                             timeout=3)
    print(response.text)
except requests.exceptions.RequestException as e:  #
    print(str(e))

if response.text == "Login in success" or response.text == "Create account success":
    # TODO: 先设置客户端的一些信息，默认已经设置好

    # 这里可以新建一个线程用于循环发送数据
    while True:
        # 客户端连接请求
        try:
            # 循环发送客户端的数据信息，设置3s超时    
            r= requests.post("http://127.0.0.1:5000/client",data=client_data,timeout=3)
            # r就是接收到的数据。r.text指把收到的content转为str
            print("client respons:",r.text)
        except exceptions.Timeout as e:
            print(str(e))
        # 如果断线，等待3s后重连    
        except exceptions.ConnectionError as e:
            print(str(e))
            time.sleep(3)
        time.sleep(1)