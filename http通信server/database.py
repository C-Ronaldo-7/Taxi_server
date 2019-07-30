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
def build_mysql(table_name, sql):
    db = connect_mysql("localhost", "glory", "0013", "newtaxi")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    if cursor.execute("show tables like '%s'; " % table_name):
        print("The table %s has be in this database! Do NOT create twice!" %
              table_name)
        db.close()
        return False
    cursor.execute(sql)
    db.close()
    return True


# 插入dict格式数据进入表中(dict顺序需要与数据库中顺序一致)
def write_sql(tabel, data):
    db = connect_mysql("localhost", "glory", "0013", "newtaxi")
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
        db.close()
        return False
    db.close()
    return True


# 根据某一主值，跟新table中其他变量
def update_sql( id, id_value, table, data):
    db = connect_mysql("localhost", "glory", "0013", "newtaxi")
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
                db.close()
                return False
    db.close()
    return True


# 根据某一主值，读取数据表中信息,返回dict数据
def read_sql(id, id_value, table):
    db = connect_mysql("localhost", "glory", "0013", "newtaxi")
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
        table=table, database="newtaxi")
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
            col_name.append(str(columns_name[i])[-3:-1])
            col_name[2*i+1]=int(col_name[2*i+1].lstrip())
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
        print("Error: unable to fetch data in ", table)
        db.close()
        return None
    db.close()
    return results_dict

# 根据某两个主值，查询数据表中信息，返回 主值
def find_sql(id1,id1_value,id2,id2_value,table,return_id):
    db = connect_mysql("localhost", "glory", "0013", "newtaxi")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    # 判断id_value是否为srt类型，str类型需要在外加‘’。
    # 否则可能会出现ERROR 1054 (42S22): Unknown column '...' in 'where clause'的错误。
    if isinstance(id1_value, str)==True and isinstance(id2_value, str) == False:
        sql = 'SELECT {return_id} FROM `{table}` WHERE `{id1}` = "{id1_value}" AND `{id2}` = {id2_value}'.format(return_id=return_id,table=table, id1=id1, id1_value=id1_value, id2=id2,id2_value=id2_value)
    elif isinstance(id2_value, str)==True and isinstance(id1_value, str) == False:
        sql = 'SELECT {return_id} FROM `{table}` WHERE `{id1}` = {id1_value} AND `{id2}` = "{id2_value}"'.format(return_id=return_id,table=table, id1=id1, id1_value=id1_value, id2=id2,id2_value=id2_value)
    elif isinstance(id1_value, str)==True and isinstance(id1_value, str)==True:
        sql = 'SELECT {return_id} FROM `{table}` WHERE `{id1}` = "{id1_value}" AND `{id2}` = "{id2_value}"'.format(return_id=return_id,table=table, id1=id1, id1_value=id1_value, id2=id2,id2_value=id2_value)
    else:
        sql = 'SELECT {return_id} FROM `{table}` WHERE `{id1}` = {id1_value} AND `{id2}` = {id2_value}'.format(return_id=return_id,table=table, id1=id1, id1_value=id1_value, id2=id2,id2_value=id2_value)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        print("Error: unable to fetch data in ", table)
        db.close()
        return "Error"
    db.close()    
    return results

# 使用预处理语句创建表
# 管理账号
admin_sql="""CREATE TABLE `admin`(
    admin_id             INTEGER NOT NULL,
    admin_name           VARCHAR(18) NULL,
    admin_password       VARCHAR(128) NULL,
    admin_limits         VARCHAR(4) NOT NULL,
    primary key(admin_id))"""

car_sql = """CREATE TABLE `car`(
    `car_id`               VARCHAR(32) NOT NULL,
    `current_position_x`   FLOAT NULL,
    `current_position_y`   FLOAT NULL,
    `current_velocity`     FLOAT NULL,
    `tire_pressure_left_front` FLOAT NULL,
    `tire_pressure_right_front` FLOAT NULL,
    `tire_pressure_left_behind` FLOAT NULL,
    `tire_pressure_right_behind` FLOAT NULL,
    `camera_status`        boolean NULL,
    `lidar_status`         boolean NULL,
    `ibeo_status`          boolean NULL,
    `car_status`           VARCHAR(4) NULL,
    `route`                VARCHAR(500) NULL,
    primary key(car_id))"""

# 客户端账号密码表
client_sql = """CREATE TABLE `client`(
    `phone_number` VARCHAR(11) NOT NULL,
    `password` VARCHAR(128),
    `login_or_create` BOOL,
    primary key(phone_number))"""

# 订单表
order_sql = """CREATE TABLE `order` (
    `order_id`        VARCHAR(19) NOT NULL,
    `car_id`          VARCHAR(32) NOT NULL,
    `phone_number`  VARCHAR(11) NOT NULL,
    `start_position_x`  FLOAT NULL,
    `start_position_y`  FLOAT NULL,
    `target_position_x`  FLOAT NULL,
    `target_position_y`  FLOAT NULL,
    `is_car_arrive_start`  BOOL NULL,
    `is_in_car`            BOOL NULL,
    `is_car_reach_target`   BOOL NULL,	
    `is_car_start_to_start_point` BOOL NULL,	
    `order_status`         VARCHAR(4) NOT NULL,	
    `order_creation_time`  DATETIME NULL,	
    `order_end_time`       DATETIME NULL,	
    `order_amount`         FLOAT NULL,
    primary key(order_id))"""

if __name__ == "__main__":
    # # 创建数据表
    # build_mysql(db,"admin",admin_sql)
    # build_mysql(db, "car", car_sql)
    # build_mysql(db, "client", client_sql)
    # build_mysql(db, "order", order_sql)

    # car_data={
    #   "car_id":"04d5cc6803f9e411a26a480fcfdf611a",
    #   "current_position_x": 0,
    #   "current_position_y": 0,
    #   "current_velocity": 0,
    #   "tire_pressure_left_front": 1.2,
    #   "tire_pressure_right_front": 1.2,
    #   "tire_pressure_left_behind": 1.5,
    #   "tire_pressure_right_behind": 1.5,
    #   "camera_status": False,
    #   "lidar_status": False,
    #   "ibeo_status": False,
    #   "car_status": "idle",
    #   "route":"[[0,0],[1,1],[1.5,1.5]]"
    # }
    # # 向数据表中插入一行数据
    # write_sql(db,"car",car_data)

    # car_data={
    #   "car_id":"04d5cc6803f9e411a26a480fcfdf611a",
    #   "current_position_x": 0,
    #   "current_position_y": 0,
    #   "current_velocity": 0,
    #   "tire_pressure_left_front": 1.2,
    #   "tire_pressure_right_front": 1.2,
    #   "tire_pressure_left_behind": 1.5,
    #   "tire_pressure_right_behind": 1.5,
    #   "camera_status": True,
    #   "lidar_status": True,
    #   "ibeo_status": True,
    #   "car_status": "idle",
    #   "route":"[[0,0],[1,1],[1.5,1.5]]"
    # }
    # # 跟新某主值为...的数据
    # update_sql(db,"car_id","04d5cc6803f9e411a26a480fcfdf611a","car",car_data)

    # # 根据主值读取数据库中一行数据
    # car_id="04d5cc6803f9e411a26a480fcfdf611a"
    # json=read_sql(db,"car_id",car_id,"car")
    # print(json)
    pass