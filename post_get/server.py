# -*- encoding: utf-8 -*-

# +-----------------------------------------+
# | @File    :   server.py                |
# | @Time    :   2019/06/30 19:59:07        |
# | @Author  :   Glory Huang                |
# | @Contact :   gloryhry@stu.xjtu.edu.cn   |
# +-----------------------------------------+

# here put the import lib
from flask import Flask, request
import ast
import json
import database

app = Flask(__name__)


class client_data():
    person_id = ""
    is_start_nav = False
    is_in_vehicle = False
    is_reach_target = False
    start_position = [0, 0]
    target_position = [1, 1]

    def __init__(self, json):
        self.person_id = json["person_id"]
        self.is_start_nav = json["is_start_nav"]
        self.is_in_vehicle = json["is_in_vehicle"]
        self.is_reach_target = json["is_reach_target"]
        self.start_position = [
            json["start_position_x"], json["start_position_y"]
        ]
        self.target_position = [
            json["target_position_x"], json["target_position_y"]
        ]

    def client_data2json(self):
        json_data = '"person_id":{person_id},"is_start_nav": {is_start_nav},"is_in_vehicle": {is_in_vehicle},"is_reach_target": {is_reach_target},"start_position_x": {start_position_x},"start_position_y": {start_position_y},"target_position_x": {target_position_x},"target_position_y": {target_position_y}'.format(
            person_id=self.person_id,
            is_start_nav=self.is_start_nav,
            is_in_vehicle=self.is_in_vehicle,
            is_reach_target=self.is_reach_target,
            start_position_x=self.start_position[0],
            start_position_y=self.start_position[1],
            target_position_x=self.target_position[0],
            target_position_y=self.target_position[1])
        # print(json_data)
        json_data = "{" + json_data + "}"
        result = ast.literal_eval(json_data)
        # print(result)
        return json.dumps(result)


class car_data():
    car_id = ""
    current_position = [0.0, 0.0]
    routine = []
    velocity = 0.0
    gas = 0.0
    pressure_left_front = 0.0
    pressure_right_front = 0.0
    pressure_left_behind = 0.0
    pressure_right_behind = 0.0
    camera_status = 0.0
    lidar_status = False
    ibeo_status = False

    def __init__(self, json):
        self.car_id = json["car_id"]
        self.current_position = [
            json["current_position_x"], json["current_position_y"]
        ]
        self.routine = ast.literal_eval(
            json["routine"])  # TODO: json中routine是str格式，转为list
        self.velocity = json["velocity"]
        self.gas = json["gas"]
        self.pressure_left_front = json["pressure_left_front"]
        self.pressure_left_behind = json["pressure_left_behind"]
        self.pressure_right_front = json["pressure_right_front"]
        self.pressure_right_behind = json["pressure_right_behind"]
        self.camera_status = json["camera_status"]
        self.lidar_status = json["lidar_status"]
        self.ibeo_status = json["ibeo_status"]

    def car_data2json(self):
        json_data = '"car_id":{car_id},"current_position_x": {current_position_x},"current_position_y": {current_position_y},"routine": {routine},"velocity": {velocity},"gas": {gas},"pressure_left_front": {pressure_left_front},"pressure_left_behind": {pressure_left_behind},"pressure_right_front": {pressure_right_front},"pressure_right_behind":{pressure_right_behind},"camera_status":{camera_status},"lidar_status":{lidar_status},"ibeo_status":{ibeo_status}'.format(
            car_id=self.car_id,
            current_position_x=self.current_position[0],
            current_position_y=self.current_position[1],
            routine=str(self.routine),
            velocity=self.velocity,
            gas=self.gas,
            pressure_left_front=self.pressure_left_front,
            pressure_left_behind=self.pressure_left_behind,
            pressure_right_front=self.pressure_right_front,
            pressure_right_behind=self.pressure_right_behind,
            camera_status=self.camera_status,
            lidar_status=self.lidar_status,
            ibeo_status=self.ibeo_status)
        json_data = "{" + json_data + "}"
        result = ast.literal_eval(json_data)
        return json.dumps(result)

class client_login_data():
    account=""
    password=""
    login_or_create=True
    def __init__(self, json):
        self.account=json["account"]
        self.password=json["password"]
        if json["login_or_create"]=="True":
            self.login_or_create=True
        else:
            self.login_or_create=False
    def data2dist(self):
        dist_data={}
        dist_data["account"]=self.account
        dist_data["password"]=self.password
        dist_data["login_or_create"]=self.login_or_create
        return dist_data


@app.route('/')
def hello_world():
    car1=car_data({"car_id": 1, "current_position_x": 0, "current_position_y": 5, "routine": "[[0,0],[1,2]]", "velocity": 1.2, "gas": 0.2, "pressure_left_front": 0.2, "pressure_left_behind": 1.9, "pressure_right_front": 1.9, "pressure_right_behind": 4.6, "camera_status": False, "lidar_status": False, "ibeo_status": False})
    return car1.car_data2json()

@app.route('/client', methods=['POST'])
def client_post():
    client = client_data(request.form)
    print(client.person_id)
    # TODO: 得到客户端需要返回的数据
    return client.client_data2json()  # 先返回输入值

@app.route('/client/login',methods=['POST'])
def client_login():
    client=client_login_data(request.form) # 获取客户端post的数据
    if client.login_or_create==True:
        dict_account=database.read_sql(db,"account",client.account,"ACCOUNT")
        # 查询数据库中有无此账号
        if dict_account==None:
            return "无此账户"
        # 检查数据库中账号密码是否正确    
        if dict_account["password"]==client.password: 
            return "Login in success"
        else:
            return "账号或密码不正确"
    elif client.login_or_create==False:
        # 检查数据库中是否有账户
        print(client.account)
        dict_account=database.read_sql(db,"account",client.account,"ACCOUNT")
        if dict_account != None:
            return "已存在此账号，请登录"
        else:
            print(client.data2dist())
            print(dict_account)
            a=database.write_sql(db,"ACCOUNT",client.data2dist()) # 写client进入数据库
            if a == True:
                return "Create account success"
            else:
                return "error occures"
    else:
        print(client.login_or_create+"?")
        return "Error occurs"



@app.route('/ROS', methods=['POST'])
def ROS_post():
    car = car_data(request.form)
    print(car.car_id)
    # TODO: 得到客户端需要返回的数据
    return car.car_data2json()


if __name__ == '__main__':
    db = database.connect_mysql("localhost", "glory", "0013", "taxi")
    app.run(port=5000, debug=True)
    