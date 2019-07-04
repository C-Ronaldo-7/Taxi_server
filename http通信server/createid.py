# -*- encoding: utf-8 -*-

# +-----------------------------------------+
# | @File    :   createid.py                |
# | @Time    :   2019/07/04 13:54:54        |
# | @Author  :   Glory Huang                |
# | @Contact :   gloryhry@stu.xjtu.edu.cn   |
# +-----------------------------------------+

# 用于生成订单编号
# here put the import lib
import time

def get_id(phone_number):
    # id格式采用时间戳与手机号间隔的方式确定订单号
    # 获取2019-1-1 00:00:00的时间戳
    tss1 = '2019-1-1 00:00:00'
    timeArray = time.strptime(tss1, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    # print(timeStamp)

    # 获取当前时间的时间戳
    now=int(time.time())
    # print(now)

    t=str(now-timeStamp)
    
    # print(t)
    phone1=phone_number[:3]
    phone2=phone_number[3:7]
    phone3=phone_number[7:9]
    phone4=phone_number[9:11]
    # print(phone1)
    # print(phone2)
    # print(phone3)
    # print(phone4)

    id= t[:-5]+phone1+t[-5:-4]+phone2+t[-4:-3]+phone3+t[-3:-2]+phone4+t[-2:]
    # print(id)
    # print (len(id))
    return id

if __name__ == "__main__":
    id=get_id("17691053351")
    print(id)