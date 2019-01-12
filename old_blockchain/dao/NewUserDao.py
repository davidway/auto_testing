# encoding=#utf-8

from pymysql import connect
from dao import BaseDao
from model import UserInfo
from model import UserAccountQueryDto
import time
from model import UserAccountCheck
from model import UserAsset
from model import GLOBAL_CONFIG
import requests
import json
headers = {
    'Accept': "application/json",
    'Content-Type': "application/json;charset=UTF-8"
}
globalConfig = GLOBAL_CONFIG.GLOBAL_CONFIG()
host = globalConfig.host
baseDao = BaseDao.BaseDao()


class NewUserDao(BaseDao.BaseDao):
    def findUserInfo(self, customerName):
        sql = """
               select id,name,address,publicKey,privateKey from user a left join user_info b  on a.id = b.userId  where customerName = %s
                and b.isBoss=1
           """
        array = []
        param = []
        param.append(customerName)
        try:

            result = baseDao.executeGetAllSql(sql, param)

            for row in result:
                user = UserInfo.UserInfo()
                user.id = row[0]
                user.name = row[1]
                user.address = row[2]
                user.privateKey = row[4]
                user.publicKey = row[3]
                array.append(user)
            return array
        except Exception as e:
            print(e)

    def getBossAccount(self,customerName):
        sql = """
                       select id,name,address,publicKey,privateKey from user a left join user_info b  on a.id = b.userId  where customerName = %s
                        and b.isBoss=0
                   """
        array = []
        param = []
        param.append(customerName)
        try:
            baseDao = BaseDao.BaseDao()
            result = baseDao.execteGetOneSql(sql,param)
            user = UserInfo.UserInfo()
            user.id = result[0]
            user.name = result[1]
            user.address = result[2]
            user.privateKey = result[4]
            user.publicKey = result[3]

            return user
        except Exception as e:
            print(e)

    def findUserInfoByAddress(self,address):
        sql = """
                       select id,name,address,publicKey,privateKey from user a left join user_info b  on a.id = b.userId  where address = %s
                   """
        array = []
        param = []
        param.append(address)
        try:
            baseDao = BaseDao.BaseDao()
            result = baseDao.execteGetOneSql(sql,param)
            user = UserInfo.UserInfo()
            user.id = result[0]
            user.name = result[1]
            user.address = result[2]
            user.privateKey = result[4]
            user.publicKey = result[3]
            return user
        except Exception as e:
            print(e)

    def baasCreateUser(self, userJson):

        url = host+"/user/addUserHasBaseAccount"
        data = userJson

        result = baseDao.safeRequests(url, data, headers, "")

        if result.status_code == 200:
            jsonResult = result.json()

            if (jsonResult['retcode'] != 0):
                raise Exception("请求错误，请查看信息:", jsonResult)
            if jsonResult['data'] != '':
                return jsonResult['data']
        pass

    def update(self, userInfo):
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
            result = baseDao.executeGetAllSql(sql, array)
            print(result)

            return result
        except Exception as e:
            print(e)

    def issue(self, issueObject):
        url = host+'/asset/issue'
        issueObject = issueObject.__dict__
        # 打印字典

        # 字典转化为json
        issueJson = json.dumps(issueObject)

        data = issueJson

        result = baseDao.safeRequests(url, data, headers, "")

        if result.status_code == 200:
            jsonResult = result.json()

            if (jsonResult['retcode'] != 0):
                raise Exception("请求错误，请查看信息:", jsonResult)
            if jsonResult['data'] != '':
                return jsonResult['data']
        pass

    def transfer(self, transferObject):
        url = host+'/asset/transfer'
        transferObjectDict = transferObject.__dict__
        # 打印字典
        # 字典转化为json
        transferObjectJson = json.dumps(transferObjectDict)
        data = transferObjectJson
        print("transferJson=",data)
        result = baseDao.safeRequests(url, data, headers, "")
        if result.status_code == 200:
            jsonResult = result.json()
            print(jsonResult)
            if (jsonResult['retcode'] != 0):
                raise Exception("请求错误，请查看信息:", jsonResult)
            if jsonResult['data'] != '':
                srcUserAsset = UserAsset.UserAsset()
                toUserAsset = UserAsset.UserAsset()
                feeUserAsset = UserAsset.UserAsset()
                dataResult = jsonResult['data']

                srcUserAsset.userAddress = transferObject.srcAccount
                srcUserAsset.assetAddress = dataResult['srcAssetId']

                toUserAsset.userAddress = transferObject.dstAccount
                toUserAsset.assetAddress = dataResult['dstAssetId']
                toUserAsset.money = transferObject.amount

                feeUserAsset.userAddress = transferObject.feeAccount
                feeUserAsset.assetAddress = dataResult['feeAssetId']
                feeUserAsset.money = transferObject.feeAmount
                return srcUserAsset, toUserAsset,feeUserAsset
        return

    def settle(self, settleObject):
        url = host+'/asset/settle'
        settleObjectDict = settleObject.__dict__
        # 打印字典

        # 字典转化为json
        settleObjectJson = json.dumps(settleObjectDict)

        data = settleObjectJson

        result = baseDao.safeRequests(url, data, headers, "")
        print(result)
        if result.status_code == 200:
            jsonResult = result.json()
            if (jsonResult['retcode'] != 0):
                raise Exception("请求错误，请查看信息:", jsonResult)
            if jsonResult['data'] != '':
                srcUserAsset = UserAsset.UserAsset()
                dataResult = jsonResult['data']

                srcUserAsset.userAddress = settleObject.ownerAccount
                srcUserAsset.assetAddress = dataResult['srcAssetId']
                return srcUserAsset

    def updateAsset(self, usertAssetObject):
        sql = """
             UPDATE `old_blockchain`.`user_asset`
             SET 

              `status` = %s

             WHERE
                 userAddress=%s and
                 `assetAddress` = %s
             LIMIT 1;
             """
        array = []
        array.append(usertAssetObject.status)
        array.append(usertAssetObject.userAddress)
        array.append(usertAssetObject.assetAddress)
        try:
            baseDao = BaseDao.BaseDao()
            result = baseDao.executeGetAllSql(sql, array)
            print(result)

            return result
        except Exception as e:
            print(e)
        return

    def insertUserAsset(self, userAsset):
        sql = """
                 INSERT INTO `old_blockchain`.`user_asset` (
                    `userAddress`,
                    `assetAddress`,
                    `status`,
                    `money`
                   )
                   VALUES
                    (%s, %s, %s,  %s);
                """
        array = []
        array.append(userAsset.userAddress)
        array.append(userAsset.assetAddress)
        array.append(userAsset.status)
        array.append(userAsset.money)

        try:

            result = baseDao.executeGetAllSql(sql, array)
            print(result)
            return result
        except Exception as e:
            print(e)
        return

    def findAssetId(self, userAsset):
        sql = """
                   select userAddress,assetAddress,money from user_asset  where status=0 and userAddress =%s limit 0,5
                   """
        array = []
        param = []
        param.append(userAsset.userAddress)
        try:
            baseDao = BaseDao.BaseDao()
            result = baseDao.executeGetAllSql(sql, param)

            for row in result:
                newUserAsset = UserAsset.UserAsset()
                newUserAsset.userAddress = row[0]
                newUserAsset.assetAddress = row[1]
                newUserAsset.money = row[2]
                array.append(newUserAsset)
            return array
        except Exception as e:
            print(e)
        return

    def getUserAccountCheckFromSql(self,userInfo):
        sql="""
            SELECT
                userAddress,
                sum(money),
                GROUP_CONCAT(
                    if ( status=0 and assetAddress!="",assetAddress,null)
                )
            FROM
                user_asset
            LEFT JOIN user_info ON user_asset.userAddress = user_info.address
            WHERE
                userAddress=%s
            AND createTime > '2019-01-04 00:00:00'
            GROUP BY userAddress
            ORDER BY
                createTime DESC
        """
        array = []
        param = []

        param.append(userInfo.address)
        print(sql)
        try:
            baseDao = BaseDao.BaseDao()
            result = baseDao.execteGetOneSql(sql, param)
            userAccountCheck = UserAccountCheck.UserAccountCheck()
            userAccountCheck.address = result[0]
            userAccountCheck.money = result[1]
            userAccountCheck.assetAddress = result[2]
            return userAccountCheck
        except Exception as e:
            print(e)
        pass

    def getUserAccountFromBass(self,userInfo):
        url = host + '/user/accountQuery'
        userAccount = UserAccountQueryDto.UserAccountQueryDto()
        # 打印字典
        userAccount.assetAccount=userInfo.address
        userAccount.state=0
        userAccount.pageLimit=20
        userAccount.pageNo=1
        # 字典转化为json
        userAccountDict = userAccount.__dict__
        userAccountJson = json.dumps(userAccountDict)

        data = userAccountJson
        print(data)
        result = baseDao.safeRequests(url, data, headers, "")

        userAccountCheck = UserAccountCheck.UserAccountCheck()
        if result.status_code == 200:
            jsonResult = result.json()

            if (jsonResult['retcode'] != 0):
                raise Exception("请求错误，请查看信息:", jsonResult)
            first=True
            money = 0
            assetAddress=""
            userAccountCheck = UserAccountCheck.UserAccountCheck()
            address=""
            if jsonResult['data'] != '':
                for each in jsonResult['data']:
                    if first:
                        assetAddress = assetAddress+each['assetId']
                        first = False
                    else:
                        assetAddress = assetAddress +","+ each['assetId']
                    money = money+each["amount"]
                    address = each["assetAccount"]
                userAccountCheck.money = money
                userAccountCheck.assetAddress = assetAddress
                userAccountCheck.address =address
                return userAccountCheck

