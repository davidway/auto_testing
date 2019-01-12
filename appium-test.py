import os
from appium import webdriver
import time
from ddt import ddt, data
from pymysql import connect
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


@ddt
class YunZiTest(unittest.TestCase):

  def setUp(self):
    desired_caps = {
      "platformName": "Android",
      "deviceName": "Honor 9",
      "appPackage": "com.dgwsy.blockchain.yunzai",
      "appActivity": "com.dgwsy.restaurantassistant.activity.LunchActivity",
      "platformVersion": "8.0.0",
    "app":"D:/yunzai.apk"

    }
    time.sleep(10)
    self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    contexts = self.driver.contexts
    print(contexts)
    self.driver.switch_to.context(contexts[1])

  # 返回一个list
  def test_tearDown(self):
    pass

  def test_qiandao(self):
      print("签到验证中")
      pass

  def test_useTool(self):
      print("使用工具中")
      pass

  @data(*getMySQLTestData())
  def test_dig(self,sqlData):
    username, password = sqlData
    time.sleep(7)
    usernameElement = self.driver.find_element_by_css_selector('#Loginput >div.inputbox >div.ipt >input[type="text"]')
    usernameElement.send_keys(username)
    passwordElement = self.driver.find_element_by_css_selector(
      '#Loginput>div.inputbox>div.ipt>input[type="password"]')
    passwordElement.send_keys(password)

    time.sleep(5)
    buttonElement = self.driver.find_element_by_css_selector("#Logphone > button")

    buttonElement.click()
    for loopTimes in range(0, 5):
      time.sleep(2)
      for num in range(0, 10):
        try:
          pathText = "#top > div.mining-main > div > div.float-box.animated.position_" + str(num) + " > button"
          print(pathText)
          #传入locator， 验证元素是否出现，只要一个符合条件的元素加载出来就通过
          kuangElement = WebDriverWait(self.driver, 10).until(
              EC.element_to_be_clickable((By.CSS_SELECTOR,pathText))
          )
          kuangElement.click()
          time.sleep(1)
        except Exception as err:
          continue
     #测试是否挖矿完成，如果不是，则记录异常
    usernameElement = self.driver.find_element_by_css_selector('#top > div.mining-main > div > span')
    if (usernameElement.text=="正在生产中"):
        print("success,"+usernameElement.text)
        pass
    else:
        print("不正常")


if __name__ == '__main__':
     suite = unittest.defaultTestLoader.loadTestsFromTestCase(YunZiTest)
     unittest.TextTestRunner().run(suite)
