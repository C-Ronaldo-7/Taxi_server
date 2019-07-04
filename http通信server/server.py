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
import threading
import createid

app = Flask(__name__)


@app.route('/')
def hello_world():
    return app.send_static_file('github404.html')


@app.route('/client', methods=['POST'])
def client_post():
    recv = str(request.data, encoding="utf-8")  # 获取客户端post的数据
    dict_data = json.loads(recv)
    # 更新order数据表
    with order_lock:
        database.update_sql(db,"order_id",dict_data["order_id"],"order",dict_data)
    order_data=database.read_sql(db,"order_id",dict_data["order_id"],"order")
    if order_data["order_status"]=="comp": # 当乘客下车后，设置car_status为idle
        with car_lock:
            car_data={}
            car_data["car_id"]=order_data["car_id"]
            car_data["car_status"]="idle"
            database.update_sql(db,"car_id",car_data["car_id"],"car",car_data)
        with order_lock:
            order_data["order_end_time"]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            database.update_sql(db,"order_id",order_data["order_id"],"order",order_data)
    order_data["order_creation_time"]=str(order_data["order_creation_time"])
    order_data["order_end_time"]=str(order_data["order_end_time"])    
    # TODO: 若需要传送回car的数据,则把car的dict和进order_data
    data={}
    car=database.read_sql(db,"car_id",order_data["car_id"],"car")
    for k,v in order_data.items():
        data[k]=v
    for k,v in car.items():
        data[k]=v
    return json.dumps(data)
    # return json.dumps(order_data)


@app.route('/client/checkorder', methods=['POST'])
def client_check():
    recv = str(request.data, encoding="utf-8")  # 获取客户端post的数据
    dict_data = json.loads(recv)
    # print(dict_data)
    # 查询是否有订单正在进行
    order_id = database.find_sql(db, "phone_number", dict_data["phone_number"],
                                 "order_status", "proc", "order", "order_id")
    # print(order_id)
    if len(order_id) != 0:  # 如果存在未完成订单，则读取订单数据发送回去
        order_data = database.read_sql(db, "order_id", order_id[0][0], "order")
        # json格式没法存储datetime类型的数据，要进行转化
        # print(order_data["order_creation_time"])
        order_data["order_creation_time"]=str(order_data["order_creation_time"])
        order_data["order_end_time"]=str(order_data["order_end_time"])
        return json.dumps(order_data)
    else:
        return "当前没有订单"

@app.route('/client/createorder',methods=['POST'])
def client_create():
    recv = str(request.data, encoding="utf-8")  # 获取客户端post的数据
    dict_data = json.loads(recv)

    # 创建新的一个订单
    order_data = {}
    car=database.read_sql(db,"car_status","idle","car")
    if car==None: # 如果数据库中找不到空闲车辆
        return "当前没有空闲车辆"
    for item in dict_data.keys():
        order_data[item]=dict_data[item]
    # 生成一个19位订单编号
    order_data["order_id"]=createid.get_id(dict_data["phone_number"])
    order_data["order_status"] = "proc"
    order_data["car_id"]=car["car_id"]
    # 更改车辆的状态为proc
    car["car_status"]="proc"
    with car_lock:
        database.update_sql(db,"car_id",car["car_id"],"car",car)
    order_data["order_creation_time"]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # print(order_data)
    # 写入order_data
    with order_lock:
        database.write_sql(db,"order",order_data)
    order_data_read=database.read_sql(db,"order_id",order_data["order_id"],"order")
    order_data_read["order_creation_time"]=str(order_data_read["order_creation_time"])
    order_data_read["order_end_time"]=str(order_data_read["order_end_time"])
    return json.dumps(order_data_read)


@app.route('/client/login', methods=['POST'])
def client_login():
    recv = str(request.data, encoding="utf-8")  # 获取客户端post的数据
    dict_data = json.loads(recv)
    # print(type(dict_data))
    # print(dict_data["login_or_create"])
    if dict_data["login_or_create"] == True:
        dict_account = database.read_sql(db, "phone_number",
                                         dict_data["phone_number"], "client")
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
        dict_account = database.read_sql(db, "phone_number",
                                         dict_data["phone_number"], "client")
        if dict_account != None:
            return "已存在此账号，请登录"
        else:
            # print(client.data2dist())
            # print(dict_account)
            a = database.write_sql(db, "client", dict_data)  # 写client进入数据库
            if a == True:
                return "Create account success"
            else:
                return "error occures"
    else:
        # print(client.login_or_create+"?")
        return "Error occurs"


@app.route('/ROS', methods=['POST'])
def ROS_post():
    recv = str(request.data, encoding="utf-8")  # 获取ROS客户端post的数据
    recv_data = json.loads(recv)
    # 取出要存入car表的值
    car_key = {
        "car_id", "current_position_x", "current_position_y",
        "current_velocity", "tire_pressure_left_front",
        "tire_pressure_right_front", "tire_pressure_left_behind",
        "tire_pressure_right_behind", "camera_status", "lidar_status",
        "ibeo_status", "route"
    }
    dict_data = {
        key: value
        for key, value in recv_data.items() if key in car_key
    }
    # 取出要存入order表的值
    order_key = {
        "car_id", "is_car_arrive_start", "is_car_reach_target",
        "is_car_start_to_start_point"
    }
    order_data = {
        key: value
        for key, value in recv_data.items() if key in order_key
    }
    # print(order_data)
    # print(dict_data)
    # 判断是否有这辆车的信息，若有则更新这car在数据库中的信息，
    if database.read_sql(db, "car_id", dict_data["car_id"], "car") == None:
        return "数据库中没有此车信息，请注册"
    else:
        # 更新这car在数据库中的信息
        if "car_status" in recv_data.keys():
            with car_lock:  #获取car锁
                database.update_sql(db, "car_id", recv_data["car_id"], "car",
                                    recv_data)
            return "跟新车辆状态成功"
        else:
            with car_lock:  #获取car锁
                database.update_sql(db, "car_id", dict_data["car_id"], "car",
                                    dict_data)
        # 查询当前车辆状态
        car_data = database.read_sql(db, "car_id", dict_data["car_id"], "car")
        if car_data["car_status"] == "idle":
            return "当前没有订单"
        elif car_data["car_status"] == "proc":
            with order_lock:  # 获取order锁
                # 跟新order表数据
                database.update_sql(db, "car_id", order_data["car_id"],
                                    "order", order_data)
        else:
            return "Error occurs"  # 车辆既没有在空闲状态，也不在订单状态
    # 得到客户端需要返回的数据
    order = database.read_sql(db, "car_id", dict_data["car_id"], "order")
    order["order_creation_time"]=str(order["order_creation_time"])
    order["order_end_time"]=str(order["order_end_time"])    
    return json.dumps(order)


@app.route('/ROS/register', methods=['POST'])
def ROS_register():
    recv = str(request.data, encoding="utf-8")
    print(recv)
    recv_data = json.loads(recv)
    # 取出要存入car表的值
    car_key = {
        "car_id", "current_position_x", "current_position_y",
        "current_velocity", "tire_pressure_left_front",
        "tire_pressure_right_front", "tire_pressure_left_behind",
        "tire_pressure_right_behind", "camera_status", "lidar_status",
        "ibeo_status", "route"
    }
    dict_data = {
        key: value
        for key, value in recv_data.items() if key in car_key
    }
    # ROS=data_define.ROS_data(dict_data)
    # 查询数据库中是否有ROS.car_id
    database_ROS = database.read_sql(db, "car_id", dict_data["car_id"], "car")
    if database_ROS != None:
        return "数据库中已有此车信息，请更新"
    else:
        with car_lock:
            resulte=database.write_sql(db, "car", dict_data)
        if resulte:
            return "车辆注册成功"
        else:
            return "Error occurs！"


db = database.connect_mysql("localhost", "glory", "0013", "taxi")
order_lock = threading.Lock()  # 创建order表的锁
car_lock = threading.Lock()
if __name__ == '__main__':
    app.run(port=5000, debug=True)
    db.close()
