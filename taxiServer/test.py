#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# @File    :   test.py
# @Time    :   2019/06/27 15:47:40
# @Author  :   Glory Huang
# @Contact :   gloryhry@stu.xjtu.edu.cn

# here put the import lib
# import json

# order_data = {
#     "car_id": 0,
#     "person_id": "0000",
#     "is_start_nav": False,
#     "is_arrive_start": False,
#     "is_in_vehicle": False,
#     "is_reach_target": False,
#     "start_position": [0, 0],
#     "target_position": [1, 1]
# }

# get_data = {
#     "car_id": 1,
#     "person_id": "0001",
#     "is_start_nav": True,
#     "is_arrive_start": False,
#     "is_in_vehicle": True,
#     "is_reach_target": False,
#     "start_position": [0, 1],
#     "target_position": [2, 1]
# }
# s=json.dumps(order_data)
# a=json.loads(s)
# print(get_data)
# for b in a.keys():
#     get_data[b]=order_data[b]
# print(get_data)

#####################################
#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# +-----------------------------------------+
# | @File    :   test.py                    |
# | @Time    :   2019/06/28 08:58:49        |
# | @Author  :   Glory Huang                |
# | @Contact :   gloryhry@stu.xjtu.edu.cn   |
# +-----------------------------------------+

# here put the import lib
import pymysql


#连接数据库
def connect_mysql(server_host, sql_user, sql_password, sql_database):
    db = pymysql.connect(host=server_host,
                         user=sql_user,
                         password=sql_password,
                         database=sql_database,
                         charset="utf8")
    return db


#创建数据表
def build_mysql(db, table_name, sql):

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    if cursor.execute("show tables like '%s'; " % table_name):
        print("The table %s has be in this database! Do NOT create twice!" % table_name)
        return False

    # # 使用 execute() 方法执行 SQL，如果表存在则删除
    # cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

    cursor.execute(sql)
    return True

# 写入json格式数据进入表中
def write_sql(db,json):
    pass

# 使用预处理语句创建表
# routine不知道有多长暂定50字节长度
car_sql = """CREATE TABLE `CAR` (
    `car_id` INT NOT NULL AUTO_INCREMENT,
    `current_position_x`  FLOAT, 
    `current_position_y`  FLOAT, 
    `routine`  VARCHAR(50),
    `velocity`  FLOAT,
    `gas`  FLOAT,
    `pressure_left_front`  FLOAT,
    `pressure_right_front`  FLOAT,
    `pressure_left_behind`  FLOAT,
    `pressure_right_behind`  FLOAT,
    `camera_status`  BOOL,
    `lidar_status`  BOOL,
    `ibeo_status`  BOOL,
    primary key(car_id))"""

# 客户端的person_id使用uuid，UUID中有固定的四个 ”-“，字符长度为32
client_sql = """CREATE TABLE `CLIENT` (
    `person_id`  VARCHAR(32),
    `is_start_nav`  BOOL,
    `is_in_vehicle`  BOOL,
    `is_reach_target`  BOOL,
    `start_position_x`  FLOAT,
    `start_position_y`  FLOAT,
    `target_position_x`  FLOAT,
    `target_position_y`  FLOAT,
    primary key(person_id))"""

#订单表
order_sql = """CREATE TABLE `ORDER` (
    `car_id` INT NOT NULL AUTO_INCREMENT,
    `person_id`  VARCHAR(32),
    `is_start_nav`  BOOL,
    `is_arrive_start`  BOOL,
    `is_in_vehicle`  BOOL,
    `is_reach_target`  BOOL,
    `start_position_x`  FLOAT,
    `start_position_y`  FLOAT,
    `target_position_x`  FLOAT,
    `target_position_y`  FLOAT,
    primary key(car_id) )"""

if __name__ == "__main__":
    db = connect_mysql("localhost", "glory", "0013", "taxi")

    # # 创建数据表
    # build_mysql(db, "ORDER", order_sql)
    # build_mysql(db, "CAR", car_sql)
    # build_mysql(db, "CLIENT", client_sql)

    db.close()