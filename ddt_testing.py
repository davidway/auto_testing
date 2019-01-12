import os
from appium import webdriver
import time
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from ddt import ddt, data
from pymysql import connect

import unittest


def getMySQLTestData():
    # 查询数据库的方法
    try:
        db = connect(host="localhost",
                     user="root",
                     password="123456",
                     db="test",
                     port=3306,
                     charset="utf8")
        # 打开数据库连接
        cur = db.cursor()
        # 使用cursor()方法获取操作游标
        sql = "SELECT `username`, `password` FROM user;"
        # sql语句
        cur.execute(sql)
        # 执行sql语句
        results = cur.fetchall()
        # 获取查询的结果
        db.commit()
        # 提交
        cur.close()
        # 关闭游标
        db.close()
        # 断开数据库连接
        return results
        # 返回一个list
    except Exception as e:
        print(e)



@ddt
# ddt驱动
class MyTestCase(unittest.TestCase):

    def setUp(self):
      pass

    @data(*getMySQLTestData())
    def test_something(self, sqlTestData):
        username, password = sqlTestData
        print(username,"密码是",password)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()