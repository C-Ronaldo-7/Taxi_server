# -*- encoding: utf-8 -*-

# +-----------------------------------------+
# | @File    :   client.py                  |
# | @Time    :   2019/07/01 15:04:36        |
# | @Author  :   Glory Huang                |
# | @Contact :   gloryhry@stu.xjtu.edu.cn   |
# +-----------------------------------------+

# here put the import lib
import requests
import time
from requests import exceptions
import hashlib
import json

client_data = {
    "person_id": 1,
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
account = "17691053354"  # 手机号码
password = "0012"
password = genearteMD5(password)
login_or_create = True
# 传送的dict数据
client = dict(account=account,
              password=password,
              login_or_create=login_or_create)
print(type(client["login_or_create"]))
print(time.strftime('%Y-%m-%d %H:%M:%S'))
# post传输数据时，必须用json格式的数据
json_client = json.dumps(client)
print(json_client)

# 与服务器通信，校验账号或者新建账号
try:
    response = requests.post("http://127.0.0.1:5000/client/login",
                             data=json_client,
                             timeout=3)
    print(response.text)
except requests.exceptions.RequestException as e:  #
    print(str(e))

# response.text 有以下几种情况
# 1. Login in success           账号登录成功，可以进行后续打车操作
# 2. 无此账户                    数据库中没有此账户，需要进行注册操作
# 3. 账号或密码不正确              账号或密码输入错误，需要重新输入
# 4. 已存在此账号，请登录           注册时发现账号已存在，需要直接登录
# 5. Create account success      注册账号成功，可以进行后续打车操作
# 6. error occures               注册账号时出错，需要重新注册
# 7. Error occurs                未知错误，可能是网络状况不行等情况

if response.text == "Login in success" or response.text == "Create account success":
    # TODO: 先设置客户端的一些信息，默认已经设置好

    # 这里可以新建一个线程用于循环发送数据
    while True:
        # 客户端连接请求
        try:
            # 循环发送客户端的数据信息，设置3s超时
            r = requests.post("http://127.0.0.1:5000/client",
                              data=client_data,
                              timeout=3)
            # r就是接收到的数据。r.text指把收到的content转为str
            print("client respons:", r.text)
            # str转为dict的数据格式
            order_data=json.loads(r.text)
            # 后面可以使用order_data数据，do what you want to do.


        except exceptions.Timeout as e:
            print(str(e))
        # 如果断线，等待3s后重连
        except exceptions.ConnectionError as e:
            print(str(e))
            time.sleep(3)
        time.sleep(1)