# encoding=#utf-8

from pymysql import connect
from dao import BaseDao
from model import UserInfo
import time
import requests
import json
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
    def findUserInfo(self,customerName):
        sql = """
              select id,name,address,publicKey,privateKey from user a left join user_info b  on a.id = b.userId  where customerName = %s
          """
        array=[]
        param=[]
        param.append(customerName)
        try:
            baseDao = BaseDao.BaseDao()
            result = baseDao.executeSql(sql,param)

            for row in result:
                user = UserInfo.UserInfo()
                user.id = row[0]
                user.name=row[1]
                user.address=row[2]
                user.privateKey=row[4]
                user.publicKey=row[3]
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
    def update(self,userInfo):
        sql = """
                    UPDATE `old_blockchain`.`user_info`
                        SET `publicKey` = %s,
                         `privateKey` = %s,
                         `address` = %s
                       
                        
                        WHERE
                            (ISNULL(`publicKey`))
                        AND (ISNULL(`privateKey`))
                        AND (ISNULL(`address`))
                        AND (`userId` = %s)
                        AND (
                            `customerName` = %s
                        )
                        LIMIT 1;
                 """
        array = []
        array.append(userInfo.publicKey)
        array.append(userInfo.privateKey)
        array.append(userInfo.address)
        array.append(userInfo.userId)
        array.append(userInfo.customerName)

        try:
            baseDao = BaseDao.BaseDao()
            result = baseDao.executeSql(sql,array)
            print(result)

            return result
        except Exception as e:
            print(e)
    def issue(self,issueObject):
        url = 'http://chat.wsy010.cn/blockchain/asset/issue'
        issueObject = issueObject.__dict__
        # 打印字典

        # 字典转化为json
        issueJson = json.dumps(issueObject)


        data = issueJson

        result = safeRequests(url, data, headers, "")

        if result.status_code == 200:
            jsonResult = result.json()

            if (jsonResult['retcode'] != 0):
                raise Exception("请求错误，请查看信息:", jsonResult)
            if jsonResult['data'] != '':
                return jsonResult['data']
        pass

    def transfer(self,transferObject):
        url = 'http://chat.wsy010.cn/blockchain/asset/transfer'
        transferObject = transferObject.__dict__
        # 打印字典

        # 字典转化为json
        transferObject = json.dumps(transferObject)


        data = transferObject

        result = safeRequests(url, data, headers, "")

        if result.status_code == 200:
            jsonResult = result.json()

            if (jsonResult['retcode'] != 0):
                raise Exception("请求错误，请查看信息:", jsonResult)
            if jsonResult['data'] != '':
                return jsonResult['data']
        pass

    def settle(self,settleObject):
        url = 'http://chat.wsy010.cn/blockchain/asset/settle'
        settleObject = settleObject.__dict__
        # 打印字典

        # 字典转化为json
        settleObject = json.dumps(settleObject)


        data = settleObject

        result = safeRequests(url, data, headers, "")

        if result.status_code == 200:
            jsonResult = result.json()

            if (jsonResult['retcode'] != 0):
                raise Exception("请求错误，请查看信息:", jsonResult)
            if jsonResult['data'] != '':
                return jsonResult['data']
        pass

    def updateAsset(self,usertAssetObject):
        pass
    def insertUserAsset(self,userAsset):
        sql = """
             INSERT INTO `old_blockchain`.`user_asset` (
                `userAddress`,
                `assetAddress`,
                `status`,
                `money`,
                `sourceId`
            )
            VALUES
                (%s, %s, %s,  %s,%s);
                        """
        array = []
        array.append(userAsset.userAddress)
        array.append(userAsset.assetAddress)
        array.append(userAsset.status)
        array.append(userAsset.money)
        array.append(userAsset.sourceId)

        try:
            baseDao = BaseDao.BaseDao()
            result = baseDao.executeSql(sql, array)
            print(result)

            return result
        except Exception as e:
            print(e)
