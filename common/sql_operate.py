# -*- coding: utf-8 -*-
"""
@Author : chain312
@Time : 2021/4/19 11:05 AM
@Description:数据库查询类
"""
import  pymysql

class Sql_operate(object):
    def __init__(self,host,port,name,passwd,db):
        self.host=host if host else '127.0.0.1'
        self.port=port if port else 33306
        self.user = name if name else 'root'
        self.passwd = passwd if passwd else '1234567'
        self.db = db if db else 'bgp_he'
    def connect_sql(self):
        try:
            db = pymysql.connect(host=self.host, port=self.port,user=self.user, passwd=self.passwd, db=self.db)
            # 使用cursor()方法获取操作游标
            cursor = db.cursor()
            return db,cursor
        except Exception as e:
            print(e)

    def select_sql(cursor,table,line,condition):

        try:
            if table=='device_detail':
                cursor.execute("select * from device_detail where ip = %s",(condition))
            elif table=='warning_type_rules':
                cursor.execute("select * from warning_type_rules where device = %s",(condition))
            else:
                print("sql 查询条件错误")
            results = cursor.fetchall()
            return results

        except  Exception as e:
            print(e)
        cursor.close()