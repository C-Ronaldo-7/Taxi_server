#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# @File    :   test.py
# @Time    :   2019/06/27 15:47:40
# @Author  :   Glory Huang 
# @Contact :   gloryhry@stu.xjtu.edu.cn

# here put the import lib
import json


order_data = {
    "car_id": 0,
    "person_id": "0000",
    "is_start_nav": False,
    "is_arrive_start": False,
    "is_in_vehicle": False,
    "is_reach_target": False,
    "start_position": [0, 0],
    "target_position": [1, 1]
}


get_data = {
    "car_id": 1,
    "person_id": "0001",
    "is_start_nav": True,
    "is_arrive_start": False,
    "is_in_vehicle": True,
    "is_reach_target": False,
    "start_position": [0, 1],
    "target_position": [2, 1]
}
s=json.dumps(order_data)
a=json.loads(s)
print(get_data)
for b in a.keys():
    get_data[b]=order_data[b]
print(get_data)