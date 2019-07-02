# -*- encoding: utf-8 -*-

# +-----------------------------------------+
# | @File    :   data_define.py             |
# | @Time    :   2019/07/02 11:05:38        |
# | @Author  :   Glory Huang                |
# | @Contact :   gloryhry@stu.xjtu.edu.cn   |
# +-----------------------------------------+

# here put the import lib


class client_login_data():
    account=""
    password=""
    login_or_create=True
    def __init__(self, dict_data):
        self.account=dict_data["account"]
        self.password=dict_data["password"]
        self.login_or_create=dict_data["login_or_create"]
    def data2dist(self):
        dict_data={}
        dict_data["account"]=self.account
        dict_data["password"]=self.password
        dict_data["login_or_create"]=self.login_or_create
        return dict_data

class ROS_data():
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
    # 从dict数据定义
    def __init__(self, dict_data):
        self.car_id = dict_data["car_id"]
        self.current_position = [
            dict_data["current_position_x"], dict_data["current_position_y"]
        ]
        self.routine = dict_data["routine"] # dict定义时就应该是str格式
        self.velocity = dict_data["velocity"]
        self.gas = dict_data["gas"]
        self.pressure_left_front = dict_data["pressure_left_front"]
        self.pressure_left_behind = dict_data["pressure_left_behind"]
        self.pressure_right_front = dict_data["pressure_right_front"]
        self.pressure_right_behind = dict_data["pressure_right_behind"]
        self.camera_status = dict_data["camera_status"]
        self.lidar_status = dict_data["lidar_status"]
        self.ibeo_status = dict_data["ibeo_status"]
    
    def car_data2dict(self):
        dict_data={}
        dict_data["car_id"]=self.car_id
        dict_data["current_position_x"]



    # def car_data2dict(self):
    #     dict_data = '"car_id":{car_id},"current_position_x": {current_position_x},"current_position_y": {current_position_y},"routine": {routine},"velocity": {velocity},"gas": {gas},"pressure_left_front": {pressure_left_front},"pressure_left_behind": {pressure_left_behind},"pressure_right_front": {pressure_right_front},"pressure_right_behind":{pressure_right_behind},"camera_status":{camera_status},"lidar_status":{lidar_status},"ibeo_status":{ibeo_status}'.format(
    #         car_id=self.car_id,
    #         current_position_x=self.current_position[0],
    #         current_position_y=self.current_position[1],
    #         routine=str(self.routine),
    #         velocity=self.velocity,
    #         gas=self.gas,
    #         pressure_left_front=self.pressure_left_front,
    #         pressure_left_behind=self.pressure_left_behind,
    #         pressure_right_front=self.pressure_right_front,
    #         pressure_right_behind=self.pressure_right_behind,
    #         camera_status=self.camera_status,
    #         lidar_status=self.lidar_status,
    #         ibeo_status=self.ibeo_status)
    #     dict_data = "{" + dict_data + "}"
    #     result = ast.literal_eval(dict_data)
    #     return dict.dumps(result)    