import unittest
from time import sleep

from ddt import ddt, data
from pymysql import connect
from selenium import webself.driver


def getMySQLTestData():
    # 查询数据库的方法
    db = connect(host="localhost",
                 user="root",
                 password="123456",
                 db="test",
                 port=3306,
                 charset="utf8")
    # 打开数据库连接
    cur = db.cursor()
    # 使用cursor()方法获取操作游标
    sql = "SELECT `search_word`, `search_result` FROM testdata;"
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


@ddt
# ddt驱动
class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.self.driver = webself.driver.Chrome()
        self.base_url = "https://www.baidu.com/"
        self.self.driver.get(self.base_url)
        self.self.driver.maximize_window()
        sleep(2)

    @data(*getMySQLTestData())
    # 传参
    def test_something(self, sqlTestData):
        searchTerm, searchResult = sqlTestData
        print(searchTerm,searchResult)
        self.driver = self.self.driver
        self.driver.find_element_by_xpath(".//*[@id='kw']").send_keys(searchTerm)
        self.driver.find_element_by_xpath(".//*[@id='su']").click()
        sleep(2)
        responseText = self.driver.find_element_by_xpath(".//*[@id='1']/h3/a").text
        self.assertEqual(responseText, searchResult)

    def tearDown(self):
        self.self.driver.close()
        self.self.driver.quit()

if __name__ == '__main__':
    unittest.main()