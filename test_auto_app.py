# -*- coding:utf-8 -*-

import unittest
import HTMLTestReportCN
from appium import webdriver
import time
import ddt



#测试用例

class YunzaiTest(unittest.TestCase):
    def setUp(self):
        desired_caps = {
            "platformName": "Android",
            "deviceName": "Honor 9",
            "appPackage": "com.dgwsy.blockchain.yunzai",
            "appActivity": "com.dgwsy.restaurantassistant.activity.LunchActivity",
            "platformVersion": "8.0.0",

        }
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        time.sleep(5)
        contexts = self.driver.contexts
        self.driver.switch_to.context(contexts[1])

    def tearDown(self):
        pass


    def testCase1(self):
        self.assertEqual(2,2,"testError")


    def testDig(self,username,password):
        usernameElement = self.driver.find_element_by_css_selector(
            '#Loginput >div.inputbox >div.ipt >input[type="text"]')
        usernameElement.send_keys(username)
        passwordElement = self.driver.find_element_by_css_selector(
            '#Loginput>div.inputbox>div.ipt>input[type="password"]')
        passwordElement.send_keys(password)
        buttonElement = self.driver.find_element_by_css_selector("#Logphone>button")
        buttonElement.click()
        time.sleep(3)
        for loopTimes in range(0, 5):
            for num in range(0, 10):
                try:
                    pathText = "#top > div.mining-main > div > div.float-box.animated.position_" + str(
                        num) + " > button"
                    print(pathText)
                    kuangElement = self.driver.find_element_by_css_selector(pathText)
                    kuangElement.click()

                except Exception as err:
                    print(err)
                    continue
        self.driver.implicitly_wait(30)




class APITestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCase1(self):
        self.assertEqual(2, 2, "testError")


#添加Suite
def Suite():
    #定义一个单元测试容器
    suiteTest = unittest.TestSuite()
    #将测试用例加入到容器
    suiteTest.addTest(YunzaiTest("testDig"))


    suiteTest.addTest(APITestCase("testCase1"))

    return suiteTest


if __name__ == '__main__':
    #确定生成报告的路径
    filePath ='F:/HTMLTestReportCN.html'
    fp = open(filePath,'wb')
    #生成报告的Title,描述
    runner = HTMLTestReportCN.HTMLTestRunner(
        stream=fp,
        title='自动化测试报告',
        #description='详细测试用例结果',
        tester='weekendzhu'
        )
    #运行测试用例
    runner.run(Suite())
    # 关闭文件，否则会无法生成文件
    fp.close()