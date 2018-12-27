# encoding=#utf-8

from pymysql import connect
from dao import BaseDao
from model import User
import time
import requests

headers = {
    'Accept': "application/json",
    'Content-Type': "application/json;charset=UTF-8"
}

def safeRequests(url,data,headers,cookies):
    result=""
    tryTimes=0
    while tryTimes<=3:
        try:
            result = requests.post(url,data=data,headers=headers,cookies=cookies)
            print(result)
            return result
        except Exception as e:
            print(e)
            time.sleep(2)
            tryTimes= tryTimes+1

class UserDao(BaseDao.BaseDao):
    def findUserInfo(self):
        sql = """
              select id,name from user
          """
        array=[]
        try:
            baseDao = BaseDao.BaseDao()
            result = baseDao.executeSql(sql)

            for row in result:
                user = User.User()
                user.id,user.name = row
                array.append(user)
            return array
        except Exception as e:
            print(e)

    def baasCreateUser(self,userJson):

        url = 'http://localhost:8080/blockchain/user/addUserHasBaseAccount'
        data = userJson

        result = safeRequests(url, data, headers, "")

        if result.status_code == 200:
            jsonResult = result.json()

            if (jsonResult['retcode'] != 0):
                raise Exception("请求错误，请查看信息:", jsonResult)
            if jsonResult['data'] != '':
                return jsonResult['data']
        pass
    def update(userInfo):
        pass