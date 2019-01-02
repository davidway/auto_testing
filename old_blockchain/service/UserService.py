# -*- coding: UTF-8 -*-


import json

from model import UserInfo
from dao import UserDao
from model import UserInfo
from model import IssueObject
from model import TransferObject
from model import SettleObject
from model import UserAsset
import datetime
import requests
import time


class UserService:

    def bassCreateUser(self,username,userId):
        user = UserInfo.UserInfo()
        user.name = username
        user.id = userId
        user = user.__dict__
        # 打印字典
        print(user)
        # 字典转化为json
        userJson = json.dumps(user)
        userDao = UserDao.UserDao()
        userDict = userDao.baasCreateUser(userJson)
        userInfo = UserInfo.UserInfo()
        userInfo.userId,userInfo.publicKey,userInfo.privateKey,userInfo.address = userDict["id"],userDict['basePublicKey'],userDict['basePrivateKey'],userDict['baseAccountAddress']
        return userInfo



    def findUserInfo(self,customerName):
        userDao = UserDao.UserDao()
        array =[]
        array = userDao.findUserInfo(customerName)
        return array
    def getBossAccount(self,customerName):
        userDao = UserDao.UserDao()

        user = userDao.getBossAccount(customerName)
        return user;
    def findUserInfoByAddress(self,address):
        userDao = UserDao.UserDao()

        userInfo = userDao.findUserInfoByAddress(address)
        return userInfo

    def updateUserInfo(self,userInfo):
        userDao = UserDao.UserDao()
        userDao.update(userInfo)

    def issue(self,bossAccount,amount):
        userDao = UserDao.UserDao()
        issueObject = IssueObject.IssueObject()
        issueObject.amount = amount
        issueObject.createUserAccountAddress=bossAccount.address
        issueObject.sourceId = "wsy_qian_yi_zhuan_yong_bao_wen"
        issueObject.content = "{\"wsy\":\"wsy_qian_yi_zhuan_yong_bao_wen\"}"
        issueObject.unit = "wsy_qian_yi_zhuan_yong_bao_wen"
        jsonResult = userDao.issue(issueObject)
        userAsset = UserAsset.UserAsset()
        userAsset.assetAddress,userAsset.status,userAsset.userAddress,userAsset.money,userAsset.sourceId = jsonResult['assetId'],"0",bossAccount.address,amount,issueObject.sourceId
        return userAsset



    def insertUserAsset(slef,userAsset):
        userDao = UserDao.UserDao()
        userDao.insertUserAsset(userAsset)
        return userAsset

    def transfer(self,transferObject):
        userDao = UserDao.UserDao()
        src,to,fee = userDao.transfer(transferObject)
        return src,to,fee

    def settle(self,settleObject):
        userDao = UserDao.UserDao()
        src = userDao.settle(settleObject)
        return src

    def updateAsset(self,to):
        userDao = UserDao.UserDao()
        assetAddressArray = to.assetAddress.split(",")
        for assetAddress in assetAddressArray:
            to.assetAddress = assetAddress
            usertAssetObject = UserAsset.UserAsset()
            usertAssetObject = to
            userDao.updateAsset(usertAssetObject)
        pass

    def findAssetId(self,userAddress):
        userDao = UserDao.UserDao()
        userAsset = UserAsset.UserAsset()
        userAsset.userAddress= userAddress
        userAssetArray = userDao.findAssetId(userAsset)
        return userAssetArray
def serviceTransferUnitTest():
    transferObject = TransferObject.TransferObject()
    transferObject.amount = 1
    transferObject.srcAccount = "1Q85VHWRpbd8pqa8XC4pwNeEebTNkt3qJz"
    transferObject.dstAccount = "1BYvJaTMV8ZFYsCbDCwZN8BaPyxeGqTA9E"
    transferObject.feeAccount = "1FnftYRs1XsZNQrAATk1MeoWzzeHUVFavc"
    transferObject.feeAmount = 1
    transferObject.srcAsset="26aMqAWkn9iXu3fmax3FYjqZUC64UxiE5oyFKYuUci1C2Rb"
    transferObject.userPrivateKey = "BvfwcVV+8QjEXwoMYbucZvLe4buAMP9OFCBn/wbl59s="
    userService = UserService()
    src,to,fee = userService.transfer(transferObject)
    print (src.assetAddress,",to=",to.assetAddress,",fee=",fee.assetAddress)
def updateAssetUnit(assetAddress,userAddress):
    userService = UserService()
    userAsset = UserAsset.UserAsset()
    userAsset.status=1
    userAsset.assetAddress=assetAddress
    userAsset.userAddress=userAddress
    userService.updateAsset(userAsset)
def insertAssetUnit(assetAddress,userAddress,money):
    userService = UserService()
    userAsset = UserAsset.UserAsset()
    userAsset.userAddress=userAddress
    userAsset.assetAddress=assetAddress
    userAsset.status=0
    userAsset.money=money
    userService.insertUserAsset(userAsset)
# assetAddress=""
# userAddress="1BYvJaTMV8ZFYsCbDCwZN8BaPyxeGqTA9E"
# updateAssetUnit(assetAddress,userAddress)
# assetAddress=""
# userAddress="1FnftYRs1XsZNQrAATk1MeoWzzeHUVFavc"
# updateAssetUnit(assetAddress,userAddress)
#
# assetAddress="27tSp9FHXasio7TK7bPhJuvEoVsiUHjJUMus9NLcbjtqCgz"
# userAddress="1FnftYRs1XsZNQrAATk1MeoWzzeHUVFavc"
# money =1
# insertAssetUnit(assetAddress,userAddress)
#
# assetAddress="27tSp9FHXasio7TK7bPhJuvEoVsiUHjJUMus9NLcbjtqCgz"
# userAddress="1BYvJaTMV8ZFYsCbDCwZN8BaPyxeGqTA9E"
# money =1
# insertAssetUnit(assetAddress,userAddress)
