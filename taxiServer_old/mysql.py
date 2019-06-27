#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# @File    :   mysql.py
# @Time    :   2019/06/25 20:27:08
# @Author  :   Glory Huang 
# @Contact :   gloryhry@stu.xjtu.edu.cn

# here put the import lib
import pymysql

def build_mysql(db):
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
    
    # 使用预处理语句创建表
    sql = """CREATE TABLE CARS (
            camera_status  VARCHAR(20),
            current_position  VARCHAR(20),
            gas double,  
            ibeo_status VARCHAR(20),
            is_arrive_start VARCHAR(20),
            is_in_vehicle VARCHAR(20),
            is_reach_target VARCHAR(20),
            is_start_nav VARCHAR(20),
            lidar_status VARCHAR(20),
            pressure_left_behind double,
            pressure_left_front double,
            pressure_right_behind double,
            pressure_right_front double,
            velocity double )"""
    
    cursor.execute(sql)


# 打开数据库连接
db = pymysql.connect("localhost","testuser","test123","TESTDB" )