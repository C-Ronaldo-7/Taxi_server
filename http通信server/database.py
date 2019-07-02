# -*- encoding: utf-8 -*-

# +-----------------------------------------+
# | @File    :   database.py                |
# | @Time    :   2019/06/29 14:06:17        |
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
    print(sql)
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
            if isinstance(data[items], str):
                update_items = '{item}="{item_value}"'.format(item=items,
                                                            item_value=data[items])
            else:
                update_items = "{item}={item_value}".format(item=items,
                                                            item_value=data[items])
            if isinstance(id_value, str):
                sql = 'UPDATE `{table}` SET {update_items} WHERE {id} = "{id_value}"'.format(
                    table=table,
                    update_items=update_items,
                    id=id,
                    id_value=id_value)
            else:
                sql = 'UPDATE `{table}` SET {update_items} WHERE {id} = {id_value}'.format(
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


# 根据某一主值，读取数据表中信息,返回dict数据
def read_sql(db, id, id_value, table):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    # 判断id_value是否为srt类型，str类型需要在外加‘’。
    # 否则可能会出现ERROR 1054 (42S22): Unknown column '...' in 'where clause'的错误。
    if isinstance(id_value, str):
        sql = 'SELECT * FROM `{table}` WHERE `{id}` = "{id_value}"'.format(
            table=table, id=id, id_value=id_value)
    else:
        sql = """SELECT * FROM `{table}` WHERE `{id}` = {id_value}""".format(
            table=table, id=id, id_value=id_value)
    sql_name = """select COLUMN_NAME,ORDINAL_POSITION from information_schema.COLUMNS where table_name = '{table}' and table_schema = '{database}';""".format(
        table=table, database="taxi")
    # print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchone()
        # 执行SQL语句
        cursor.execute(sql_name)
        columns_name = cursor.fetchall()
        columns_name = list(columns_name)
        # 将columns_name元祖转为列表
        col_name = []
        for i in range(len(columns_name)):
            tmp = str(columns_name[i]).split("'")
            # print(tmp)
            col_name.append(tmp[1])
            col_name.append(str(columns_name[i])[-2:-1])
        # print(col_name)
        # 先将col_name排序，排成定义的顺序
        for i in range(0, len(columns_name) - 1):
            for j in range(0, len(columns_name) - i - 1):
                if col_name[2 * j + 1] > col_name[2 * j + 3]:
                    tmp = [col_name[2 * j], col_name[2 * j + 1]]
                    col_name[2 * j] = col_name[2 * j + 2]
                    col_name[2 * j + 1] = col_name[2 * j + 3]
                    col_name[2 * j + 2] = tmp[0]
                    col_name[2 * j + 3] = tmp[1]
        # print(col_name)
        results_dict = {}
        for i in range(len(results)):
            col_name[2 * i + 1] = results[i]
        results_dict = dict(zip(col_name[::2], col_name[1::2]))
        # print(results_dict)
    except:
        print("Error: unable to fetch data")
        return None
    return results_dict


# 使用预处理语句创建表
# routine不知道有多长暂定1000字节长度
car_sql = """CREATE TABLE `CAR` (
    `car_id` VARCHAR(128) NOT NULL,
    `current_position_x`  FLOAT, 
    `current_position_y`  FLOAT, 
    `routine`  VARCHAR(1000),
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
    `person_id`  VARCHAR(11) NOT NULL,
    `is_start_nav`  BOOL,
    `is_in_vehicle`  BOOL,
    `is_reach_target`  BOOL,
    `start_position_x`  FLOAT,
    `start_position_y`  FLOAT,
    `target_position_x`  FLOAT,
    `target_position_y`  FLOAT,
    primary key(person_id))"""

# 账号密码表
account_sql = """CREATE TABLE `ACCOUNT`(
    `account` VARCHAR(11) NOT NULL,
    `password` VARCHAR(128),
    `login_or_create` BOOL,
    primary key(account))"""

# 订单表
order_sql = """CREATE TABLE `ORDER` (
    `car_id` VARCHAR(128) NOT NULL,
    `person_id`  VARCHAR(11),
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
    # build_mysql(db,"ACCOUNT",account_sql)

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
    # 跟新某主值为...的数据
    # update_sql(db,"person_id",1,"CLIENT",client_data)

    # # 根据主值读取数据库中一行数据
    # account="17691053351"
    # json=read_sql(db,"account",account,"ACCOUNT")
    # print(json)

    db.close()