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
    def updateUserInfo(self,userInfo):
        userDao = UserDao.UserDao()
        userDao.update(userInfo)

    def issue(self,bossAccount,amount):
        userDao = UserDao.UserDao()
        issueObject = IssueObject.IssueObject()
        issueObject.amount = amount
        issueObject.createUserAccountAddress=bossAccount.address
        issueObject.sourceId = "qianyi"+str(datetime.datetime.now())
        issueObject.content = "{\"wsy\":\"qianyiuse\"}"
        issueObject.unit = "qianyi"
        jsonResult = userDao.issue(issueObject)
        userAsset = UserAsset.UserAsset()
        userAsset.assetAddress,userAsset.status,userAsset.userAddress,userAsset.money,userAsset.sourceId = jsonResult['assetId'],"0",bossAccount.address,amount,issueObject.sourceId
        return userAsset

    def getBossAccount(self,list):
        for obj in list:
            if (obj.id.startswith("qianyibBos")):
                return obj

    def insertUserAsset(slef,userAsset):
        userDao = UserDao.UserDao()
        userDao.insertUserAsset(userAsset)
        return userAsset

    def transfer(self,src,to,fee,amount,feeAmount):
        userDao = UserDao.UserDao()
        transferObject = TransferObject.TransferObject()
        userDao.transfer(transferObject)
        pass
    def settle(self):
        userDao = UserDao.UserDao()
        settleObject = SettleObject.TransferObject()
        userDao.settle(settleObject)
        pass

    def updateAsset(self,to):
        userDao = UserDao.UserDao()
        usertAssetObject = UserAsset.UsertAsset()
        userDao.updateAsset(usertAssetObject)
        pass
# userService = UserService()
# baasAccount = UserInfo.UserInfo()
# baasAccount.address="143zd1h2VTWmBdZPDbCV1Sh6hne1NxDSsV"
# baasAccount.publicKey="Ato+pz0af0Kljx0Wv+cKu6jcCkN9Rmmg0oiC/VWebCQb"
# baasAccount.privateKey="LsWZ5W3VbtCtIuZ1fYkhW4kT4UY30tu82YhSOC34Qg4="
# userAsset = userService.issue(baasAccount,"1000")
# userService.insertUserAsset(userAsset)
