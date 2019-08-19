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
# import xinge

app = Flask(__name__)

# 404主页
@app.route('/')
def hello_world():
    return app.send_static_file('github404.html')

# 客户端通信
@app.route('/client', methods=['POST'])
def client_post():
    recv = str(request.data, encoding="utf-8")  # 获取客户端post的数据
    dict_data = json.loads(recv)
    # 更新order数据表
    with order_lock:
        database.update_sql("order_id", dict_data["order_id"], "taxitest_order",
                            dict_data)
    order_data = database.read_sql("order_id", dict_data["order_id"], "taxitest_order")
    # TODO: 判断车辆是否到达接客点，若到达则给客户端推送到达信息 设置account为客户端的手机号
    # push=xinge.XingeApp("a0381c28541e4","570812dd57c4d94451b1e36766db6697")
    # if order_data["is_car_arrive_start"]==Ture and order_data["is_car_reach_target"]==False :
    #     msg=xinge.MessageIOS()
    #     msg.alert="json"
    #     msg.expireTime = 3600
    #     msg.custom={}
    #     account = order_data["client_id"]
    #     ret=push.PushSingleAccount(0,account,msg,1)
    # elif order_data["is_car_reach_target"]==True:
    #     msg=xinge.MessageIOS()
    #     msg.alert="json"
    #     account = order_data["client_id"]
    #     ret=push.PushSingleAccount(0,account,msg,1)

    if order_data["order_status"] == "comp":  # 当乘客下车后，设置car_status为idle
        with car_lock:
            car_data = {}
            car_data["car_id"] = order_data["car_id"]
            car_data["car_status"] = "idle"
            database.update_sql("car_id", car_data["car_id"], "taxitest_car", car_data)
        with order_lock:
            order_data["order_end_time"] = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime())
            database.update_sql("order_id", order_data["order_id"], "taxitest_order",
                                order_data)
    order_data["order_creation_time"] = str(order_data["order_creation_time"])
    order_data["order_end_time"] = str(order_data["order_end_time"])
    # 若需要传送回car的数据,则把car的dict和进order_data
    data = {}
    car = database.read_sql("car_id", order_data["car_id"], "taxitest_car")
    for k, v in order_data.items():
        data[k] = v
    for k, v in car.items():
        data[k] = v
    return json.dumps(data)
    # return json.dumps(order_data)

# 客户端检查订单
@app.route('/client/checkorder', methods=['POST'])
def client_check():
    recv = str(request.data, encoding="utf-8")  # 获取客户端post的数据
    dict_data = json.loads(recv)
    # print(dict_data)
    # 检查是否在排队，若在排队，则返回wait_client的信息。
    wait_data=database.read_sql("phone_number",dict_data["phone_number"],"wait_client")
    if wait_data != None:
        wait_data.pop("creation_time")
        return json.dumps(wait_data)
    # 查询是否有订单正在进行
    order_id = database.find_sql("phone_number", dict_data["phone_number"],
                                 "order_status", "proc", "taxitest_order", "order_id")
    # print(order_id)
    if len(order_id) != 0:  # 如果存在未完成订单，则读取订单数据发送回去
        order_data = database.read_sql("order_id", order_id[0][0], "taxitest_order")
        # json格式没法存储datetime类型的数据，要进行转化
        # print(order_data["order_creation_time"])
        order_data["order_creation_time"] = str(
            order_data["order_creation_time"])
        order_data["order_end_time"] = str(order_data["order_end_time"])
        return json.dumps(order_data)
    else:
        return "当前没有订单"

# 客户端创建订单
@app.route('/client/createorder', methods=['POST'])
def client_create():
    recv = str(request.data, encoding="utf-8")  # 获取客户端post的数据
    dict_data = json.loads(recv)
    # 判断是否要取消排队等候
    if dict_data.has_key('queue_cancel'):
        if dict_data['queue_cancel']==True:
            if database.delete_line("phone_number",dict_data["phone_number"],"wait_client")：
                return "cancel queue success"
            else:
                return "cancel queue fail"
    # 检查是否在排队列表中，
    # 如果是，则判断排队中的位置，
    # 若为第一位，则判断有没有车辆空闲出来
    # 若不为第一位，返回当前排队的还有多少人
    rank=database.find_row("phone_number",dict_data["phone_number"],"wait_client")
    if rank != "Error":
        if rank == 1:
            car = database.read_sql("car_status", "idle", "taxitest_car")
            if car == None:
                return "当前有1人在排队"
            else:
                # 创建新的一个订单
                order_data = {}
                for item in dict_data.keys():
                    order_data[item] = dict_data[item]
                # 生成一个19位订单编号
                order_data["order_id"] = createid.get_id(dict_data["phone_number"])
                order_data["order_status"] = "proc"
                order_data["car_id"] = car["car_id"]
                # 更改车辆的状态为proc
                car["car_status"] = "proc"
                with car_lock:
                    database.update_sql("car_id", car["car_id"], "taxitest_car", car)
                order_data["order_creation_time"] = time.strftime("%Y-%m-%d %H:%M:%S",
                                                                time.localtime())
                # print(order_data)
                # 写入order_data
                with order_lock:
                    database.write_sql("taxitest_order", order_data)
                order_data_read = database.read_sql("order_id", order_data["order_id"],
                                                    "taxitest_order")
                order_data_read["order_creation_time"] = str(
                    order_data_read["order_creation_time"])
                order_data_read["order_end_time"] = str(order_data_read["order_end_time"])
                return json.dumps(order_data_read)
        elif rank >= 2:
            return "当前有{rank}人在排队".format(rank=rank)
    # 如果排队列表里没有人在排队，那么直接叫车
    # 否则加入排队列表中
    sum_wait=database.count_row("phone_number","wait_client")
    if sum_wait =="error":
        return "error"
    elif sum_wait > 0:
        wait_data={}
        for item in dict_data.keys():
            wait_data[item] = dict_data[item]
        wait_data["creation_time"] = time.time()
        database.write_sql("wait_client",wait_data)
        return "当前有{wait}人在排队".format(sum_wait+1)

    # 创建新的一个订单
    order_data = {}
    car = database.read_sql("car_status", "idle", "taxitest_car")
    if car == None:  # 如果数据库中找不到空闲车辆
        # TODO: 判断是否正在排队，若没有在排队则放入wait_client的表单中。
        return "当前没有空闲车辆"
    for item in dict_data.keys():
        order_data[item] = dict_data[item]
    # 生成一个19位订单编号
    order_data["order_id"] = createid.get_id(dict_data["phone_number"])
    order_data["order_status"] = "proc"
    order_data["car_id"] = car["car_id"]
    # 更改车辆的状态为proc
    car["car_status"] = "proc"
    with car_lock:
        database.update_sql("car_id", car["car_id"], "taxitest_car", car)
    order_data["order_creation_time"] = time.strftime("%Y-%m-%d %H:%M:%S",
                                                      time.localtime())
    # print(order_data)
    # 写入order_data
    with order_lock:
        database.write_sql("taxitest_order", order_data)
    order_data_read = database.read_sql("order_id", order_data["order_id"],
                                        "taxitest_order")
    order_data_read["order_creation_time"] = str(
        order_data_read["order_creation_time"])
    order_data_read["order_end_time"] = str(order_data_read["order_end_time"])
    return json.dumps(order_data_read)

# 客户端登录和注册(需要在进行登录注册操作时多发送一个is_client_login的标志位，默认为False)
@app.route('/client/login', methods=['POST'])
def client_login():
    recv = str(request.data, encoding="utf-8")  # 获取客户端post的数据
    dict_data = json.loads(recv)
    # print(type(dict_data))
    # print(dict_data["login_or_create"])
    if dict_data["login_or_create"] == True:
        dict_account = database.read_sql("phone_number",
                                         dict_data["phone_number"], "taxitest_client")
        # 查询数据库中有无此账号
        if dict_account == None:
            return "无此账户"
        # 检查数据库中账号密码是否正确
        elif dict_account["password"] == dict_data["password"]:
        	# 检查是否该账户已在别的设备登录
        	if dict_account["is_client_login"] == True:
        		return "此账号已在别的设备登录"
        	# 登陆成功时将数据库中对应该账号的标志位is_client_login置为True
        	else:
                dict_account["is_client_login"] = True
                with client_lock:   # 获取client锁
                    database.update_sql("phone_number", dict_account["phone_number"], 
                                        "taxitest_client", dict_account)
                return json.dumps(dict_account) # 账号登陆成功，返回账号信息
        elif dict_account["password"] != dict_data["password"]:
            return "账号或密码不正确"
    elif dict_data["login_or_create"] == False:
        # 检查数据库中是否有账户
        # print(client.account)
        dict_account = database.read_sql("phone_number",
                                         dict_data["phone_number"], "taxitest_client")
        if dict_account != None:
            return "已存在此账号，请登录"
        else:
        	if len(dict_data["username"]) == 0:
        		return "用户名不能为空"
        	else:
                flag = True
                for s in dict_data["username"]:
                    if (s >= u'\u4e00' and s<=u'\u9fff') or ((s >= u'\u0041' and s <= u'\u005a')
                        or (s >= u'\u0061' and s <= u'\u007a')) or s.isdigit():
			    	    flag = True
				    else:
				        flag = False
				        break
                if flag == True:
                    dict_data["is_client_login"] = True
                    a = database.write_sql("taxitest_client", dict_data)  # 写client进入数据库
                    if a == True:
                        dict_account = database.read_sql("phone_number",
                                                         dict_data["phone_number"], "taxitest_client")
                        return json.dumps(dict_account) # 账号注册并登陆成功，返回账号信息
                    else:
                        return "error occures"
                else:
                    return "用户名输入错误，请重新输入"           
    else:
        # print(client.login_or_create+"?")
        return "Error occurs"

# 客户端退出登录
@app.route('/client/logout', methods=['POST'])
def client_logout():
    recv = str(request.data, encoding="utf-8")  # 获取客户端post的数据
    dict_data = json.loads(recv)

    dict_account = database.read_sql("phone_number",
                                     dict_data["phone_number"], "taxitest_client")
    order_id = database.find_sql("phone_number", dict_data["phone_number"], "order_status",
                                 "proc", "taxitest_order", "order_id")
    # 检查该账号是否存在
    if dict_account == None:
        return "无此账户"
    # 检查盖该账户是否处于登录状态
    elif dict_account["is_client_login"] == False:
        return "该账号并未登录"
    # 检查该账户是否有订单正在进行
    elif len(order_id) != 0:
        return "当前有订单正在进行，无法退出登录"
    # 退出登录，设置标志位is_client_login为False
    else:
        dict_account["is_client_login"] = False
        with client_lock:  # 获取client锁
            database.update_sql("phone_number", dict_account["phone_number"], 
                                 "taxitest_client", dict_account)
        return "当前账号已成功退出"

# ROS端通信
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
    if database.read_sql("car_id", dict_data["car_id"], "taxitest_car") == None:
        return "数据库中没有此车信息，请注册"
    else:
        # 更新这car在数据库中的信息
        if "car_status" in recv_data.keys():
            with car_lock:  #获取car锁
                database.update_sql("car_id", recv_data["car_id"], "taxitest_car",
                                    recv_data)
            return "跟新车辆状态成功"
        else:
            with car_lock:  #获取car锁
                database.update_sql("car_id", dict_data["car_id"], "taxitest_car",
                                    dict_data)
        # 查询当前车辆状态
        car_data = database.read_sql("car_id", dict_data["car_id"], "taxitest_car")
        if car_data["car_status"] == "idle":
            return "当前没有订单"
        elif car_data["car_status"] == "proc":
            with order_lock:  # 获取order锁
                # 跟新order表数据
                database.update_sql("car_id", order_data["car_id"], "taxitest_order",
                                    order_data)
        else:
            return "Error occurs"  # 车辆既没有在空闲状态，也不在订单状态
    # 得到客户端需要返回的数据
    orderid = database.find_sql("car_id", dict_data["car_id"], "order_status",
                                "proc", "taxitest_order", "order_id")
    # print(orderid)
    orderid0 = orderid[0][0]
    order = database.read_sql("order_id", orderid0, "taxitest_order")
    order["order_creation_time"] = str(order["order_creation_time"])
    order["order_end_time"] = str(order["order_end_time"])
    return json.dumps(order)

# ROS端注册
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
    database_ROS = database.read_sql("car_id", dict_data["car_id"], "taxitest_car")
    if database_ROS != None:
        return "数据库中已有此车信息，请更新"
    else:
        with car_lock:
            resulte = database.write_sql("taxitest_car", dict_data)
        if resulte:
            return "车辆注册成功"
        else:
            return "Error occurs！"


order_lock = threading.Lock()  # 创建order表的锁
car_lock = threading.Lock()
client_lock = threading.Lock()
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=False)

    # # 信鸽推送test
    # push=xinge.XingeApp("a0381c28541e4","570812dd57c4d94451b1e36766db6697")
    # msg=xinge.MessageIOS()
    # msg.alert="json"
    # msg.expireTime = 3600
    # msg.custom={}
    # ret=push.PushSingleAccount(0,"17691053351",msg,2)
