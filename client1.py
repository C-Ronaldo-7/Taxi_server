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

# 设置服务器ip地址
server_host="47.111.92.117"




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
phone_number = "17691053351"  # 手机号码
password = "0013"
password = genearteMD5(password)
login_or_create = True
is_client_login = False

# 传送的dict数据
client = dict(phone_number=phone_number,
              password=password,
              login_or_create=login_or_create,
              is_client_login=is_client_login)
print(type(client["login_or_create"]))
print(time.strftime('%Y-%m-%d %H:%M:%S'))
# post传输数据时，必须用json格式的数据
json_client = json.dumps(client)
print(json_client)

# 与服务器通信，校验账号或者新建账号
try:
    response = requests.post("http://{server_host}:5000/client/login".format(server_host=server_host),
                             data=json_client,
                             timeout=10)
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

# 退出登录当前账号
'''
try:
    response = requests.post("http://{server_host}:5000/client/login".format(server_host=server_host),
                             data=json_client,
                             timeout=10)
    print(response.text)
except requests.exceptions.RequestException as e:
    print(str(e))
'''

client_data = {
    "phone_number": "17691053351",
    "start_position_x": 0.2,
    "start_position_y": 0.2,
    "target_position_x": 1.9,
    "target_position_y": 1.9,
    "is_in_car": False,
    "order_status": "proc"
}
# is_in_car 默认值应为False
# order_status 默认值应为“proc" (processing)
# order_status客户端应该直到乘客下车后才能发送"comp" (completed)


if response.text == "Login in success" or response.text == "Create account success":
    # 查询有无订单正在进行
    try:
        resv = requests.post("http://{server_host}:5000/client/checkorder".format(server_host=server_host),
                                data=json.dumps(client_data),
                                timeout=3)
        print(resv.text) # 打印返还数据
        if resv.text!="当前没有订单":
            # 返还数据库中上次订单数据，并转为list格式
            order_data=json.loads(resv.text)
            print("继续之前订单")
            # TODO: 还原之前的状态
        else:
            #之前订单完成,创建新的订单
            # TODO: 输入订单信息等
            # client_data = ...
            print("输入订单信息...")
            while True:
                try:
                    res = requests.post("http://{server_host}:5000/client/createorder".format(server_host=server_host),
                                            data=json.dumps(client_data),
                                            timeout=3)
                    print("respons order:",res.text) # 打印返还数据
                    if res.text != "当前没有空闲车辆":
                        # 返还数据库中新建的订单数据，并转为list格式
                        order_data=json.loads(res.text)
                        break
                    else:
                        #等待3s后重新下单
                        # TODO: 可以加判断是否要退出等待
                        time.sleep(3)
                
                except requests.exceptions.RequestException as e:  # 网络不畅通，重新登录
                    print(str(e))

    except requests.exceptions.RequestException as e:  #
        print(str(e))

    


    # 这里可以新建一个线程用于循环发送数据
    while True:
        # 客户端保持通信的数据传输格式
        order_send_data={
            "order_id":"",
            "start_position_x": 0.2,
            "start_position_y": 0.2,
            "target_position_x": 1.9,
            "target_position_y": 1.9,
            "is_in_car": False,
            "order_status": "proc"
        }
        # order_status 默认值应为“proc" (processing)
        # order_status客户端应该直到乘客下车后才能发送"comp" (completed)
        order_send_data["order_id"]=order_data["order_id"]
        # TODO: 记得要跟新order_send_data
        try:
            # 循环发送客户端的数据信息，设置3s超时
            r = requests.post("http://{server_host}:5000/client".format(server_host=server_host),
                              data=json.dumps(order_send_data),
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