# -*- encoding: utf-8 -*-

# +-----------------------------------------+
# | @File    :   server.py                  |
# | @Time    :   2019/07/02 11:01:52        |
# | @Author  :   Glory Huang                |
# | @Contact :   gloryhry@stu.xjtu.edu.cn   |
# +-----------------------------------------+

# here put the import lib
from flask import Flask, request
import ast
import json
import database
import time

app = Flask(__name__)


@app.route('/')
def hello_world():
    return app.send_static_file('github404.html')


# @app.route('/client', methods=['POST'])
# def client_post():
#     client = client_data(request.form)
#     print(client.person_id)
#     time.sleep(1)
#     # TODO: 得到客户端需要返回的数据
#     return client.client_data2json()  # 先返回输入值


@app.route('/client/login', methods=['POST'])
def client_login():
    recv = str(request.data, encoding="utf-8")  # 获取客户端post的数据
    dict_data = json.loads(recv)
    # print(type(dict_data))
    # print(dict_data["login_or_create"])
    # client=data_define.client_login_data(dict_data)
    if dict_data["login_or_create"] == True:
        dict_account = database.read_sql(db, "account", dict_data["account"],
                                         "ACCOUNT")
        # 查询数据库中有无此账号
        if dict_account == None:
            return "无此账户"
        # 检查数据库中账号密码是否正确
        if dict_account["password"] == dict_data["password"]:
            return "Login in success"
        else:
            return "账号或密码不正确"
    elif dict_data["login_or_create"] == False:
        # 检查数据库中是否有账户
        # print(client.account)
        dict_account = database.read_sql(db, "account", dict_data["account"],
                                         "ACCOUNT")
        if dict_account != None:
            return "已存在此账号，请登录"
        else:
            # print(client.data2dist())
            # print(dict_account)
            a = database.write_sql(db, "ACCOUNT", dict_data)  # 写client进入数据库
            if a == True:
                return "Create account success"
            else:
                return "error occures"
    else:
        # print(client.login_or_create+"?")
        return "Error occurs"


@app.route('/ROS', methods=['POST'])
def ROS_post():
    recv = str(request.data, encoding="utf-8")  # 获取客户端post的数据
    dict_data = json.loads(recv)
    print(dict_data)
    # 判断是否有这辆车的信息，若有则更新这car在数据库中的信息，
    if database.read_sql(db,"car_id",dict_data["car_id"],"CAR")==None:
        return "数据库中没有此车信息，请注册"
    else:
        # 更新这car在数据库中的信息
        database.update_sql(db,"car_id",dict_data["car_id"],"CAR",dict_data)
        pass
        # TODO: 得到客户端需要返回的数据
    order = {}
    return json.dumps(order)


@app.route('/ROS/register', methods=['POST'])
def ROS_register():
    recv = str(request.data, encoding="utf-8")
    print(recv)
    dict_data = json.loads(recv)
    # ROS=data_define.ROS_data(dict_data)
    # 查询数据库中是否有ROS.car_id
    database_ROS = database.read_sql(db, "car_id", dict_data["car_id"], "CAR")
    if database_ROS != None:
        return "数据库中已有此车信息，请更新"
    else:
        if database.write_sql(db, "CAR", dict_data):
            return "车辆注册成功"
        else:
            return "Error occurs！"


db = database.connect_mysql("localhost", "glory", "0013", "taxi")
if __name__ == '__main__':
    app.run(port=5000, debug=True)
    db.close()
