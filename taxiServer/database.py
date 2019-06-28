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


# 连接数据库
def connect_mysql(server_host, sql_user, sql_password, sql_database):
    db = pymysql.connect(host=server_host,
                         user=sql_user,
                         password=sql_password,
                         database=sql_database,
                         charset="utf8")
    return db


# 创建数据表
def build_mysql(db, table_name, sql):
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    if cursor.execute("show tables like '%s'; " % table_name):
        print("The table %s has be in this database! Do NOT create twice!" %
              table_name)
        return False
    cursor.execute(sql)
    return True


# 插入dict格式数据进入表中(dict顺序需要与数据库中顺序一致)
def write_sql(db, tabel, data):
    cursor = db.cursor()
    keys = ""
    values = ""
    for item in data.keys():
        keys = keys + " `%s`," % (item)
        if type(data[item]) == str:
            values = values + ' "' + data[item] + '",'
        else:
            values = values + ' {},'.format(data[item])
    keys = keys[:-1]
    values = values[:-1]
    # print(values)
    # print(keys)
    sql = """INSERT INTO `{table}` ({keys}) VALUES ({values})""".format(
        table=tabel, keys=keys, values=values)
    # print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
        return False
    return True


# 根据某一主值，跟新table中其他变量
def update_sql(db, id, id_value, table, data):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    for items in data.keys():
        if items != id:
            update_items = "{item}={item_value}".format(item=items,
                                                        item_value=data[items])
            sql = """UPDATE `{table}` SET {update_items} WHERE {id} = {id_value}""".format(
                table=table,
                update_items=update_items,
                id=id,
                id_value=id_value)
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                # 如果发生错误则回滚
                db.rollback()
                return False
    return True


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

# 订单表
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

    # client_data={
    #   "person_id":1,
    #   "is_start_nav": False,
    #   "is_in_vehicle": True,
    #   "is_reach_target": True,
    #   "start_position_x": 1.2,
    #   "start_position_y": 1.2,
    #   "target_position_x": 1.5,
    #   "target_position_y": 1.5
    # }
    # # 向数据表中插入一行数据
    # write_sql(db,"CLIENT",client_data)

    # client_data={
    #   "person_id":1,
    #   "is_start_nav": True,
    #   "is_in_vehicle": True,
    #   "is_reach_target": False,
    #   "start_position_x": 0.2,
    #   "start_position_y": 0.2,
    #   "target_position_x": 1.9,
    #   "target_position_y": 1.9
    # }
    # update_sql(db,"person_id",1,"CLIENT",client_data)

    db.close()