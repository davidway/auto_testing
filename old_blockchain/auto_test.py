# encoding=#utf-8
from controller import UserController
from controller import ConfigController
from model import UserAsset
from model import TransferObject
from model import SettleObject
from model import UserInfo
import json
import time
###SQL准备
"""

UPDATE user set id= left(concat(id,MD5(CURRENT_TIMESTAMP) ),12),name =  left(concat(name,MD5(CURRENT_TIMESTAMP) ),12);

delete from user_info;
insert into user_info(userId,customerName) select `user`.id,config.customerName from user,config;
"""


def setConfig(customerName):
    configController = ConfigController.ConfigController()
    config = configController.set(customerName)
    config.customerName = customerName
    if (config.ledgerId == ''):
        raise RuntimeError("设置报文出错了")
    return config

def userReigstUnit(customerName):
    config = setConfig(customerName)
    userController = UserController.UserController()
    userController.createUserList(config)

def issueTest(bossAccount,amount,customerName):
    config = setConfig(customerName)
    userController = UserController.UserController()
    userController.issue(bossAccount, amount)
    pass

def transferToAllTest(customerName,amount,feeAmount):
    try:
        userController = UserController.UserController()
        list = userController.getUserInfo(customerName)

        src = userController.getBossAccount( customerName)
        for i in range(list.__len__()):
            print("i=", i, ",item=", list.__getitem__(i).__getattribute__("id"))
            idStr = list.__getitem__(i).__getattribute__("id")
            if ( idStr.startswith("qianyibBos")==True ):
                continue
            if i % 2 == 0:
                to = {}
                fee = {}
            if i%2==0:
                to = list.__getitem__(i)
            if i%2==1:
                fee = list.__getitem__(i)
            if (to != {} and fee != {}):
                print(i, ",to=", to.__getattribute__("id"), "fee", fee.__getattribute__("id"), ",i=", i)
                userAsset = UserAsset.UserAsset()
                userAssetArray = userController.findAssetId(src)
                assetAddressArray = ""
                money = 0
                for each in userAssetArray:
                    money = int(money) + each.money
                    assetAddressArray = assetAddressArray + each.assetAddress
                transferObject = TransferObject.TransferObject()
                transferObject.srcAccount = src.address
                transferObject.dstAccount = to.address
                transferObject.feeAccount = fee.address
                transferObject.amount = amount
                transferObject.feeAmount = feeAmount
                transferObject.srcAsset = assetAddressArray
                transferObject.userPrivateKey = src.privateKey
                userController = UserController.UserController()
                src_money = money
                userController.transfer(src, to, fee, src_money, transferObject)
    except Exception as e:
        print(e)
#transferToAllTest("演示环境账本",8,8)
def settleTest(address,amount):
    userController = UserController.UserController()
    userInfo = UserInfo.UserInfo()


    settleObject =SettleObject.SettleObject()
    settleObject.amount = amount
    settleObject.ownerAccount = address

    userInfo = userController.findUserInfoByAddress(settleObject.ownerAccount)
    settleObject.userPrivateKey = userInfo.privateKey
    userAssetArray = userController.findAssetId(userInfo)
    userAssetStr = ""
    first= True
    for each in userAssetArray:
        if first:
            userAssetStr = userAssetStr+each.assetAddress
            first=False
        else:
            userAssetStr = userAssetStr+"," + each.assetAddress
    settleObject.srcAsset = userAssetStr
    userController.settle(settleObject)
def transferUser(src,to,fee,amount,feeAmount):
    userController = UserController.UserController
    userAsset = UserAsset.UserAsset()
    userAssetArray = userController.findAssetId(src)
    assetAddressArray = ""
    money = 0
    for each in userAssetArray:
        money = int(money) + each.money
        assetAddressArray = assetAddressArray + each.assetAddress
    transferObject = TransferObject.TransferObject()
    transferObject.srcAccount = src.address
    transferObject.dstAccount = to.address
    transferObject.feeAccount = fee.address
    transferObject.amount = amount
    transferObject.feeAmount = feeAmount
    transferObject.srcAsset = assetAddressArray
    transferObject.userPrivateKey = src.privateKey
    userController = UserController.UserController()
    src_money = money
    userController.transfer(src, to, fee, src_money, transferObject)

def issueUnit():
    customerName = "演示环境账本"
    bossAccount = {}
    userController = UserController.UserController()
    list = userController.getUserInfo(customerName)
    bossAccount = userController.getBossAccount(customerName)
    issueTest(bossAccount,1000,customerName)

#issueUnit()

def transferToAllUnit():
    customerName = "演示环境账本"
    transferToAllTest(customerName,8,8)
#transferToAllUnit()
def eachTransferToOther(customerName,amount,feeAmount):
    try:
        userController = UserController.UserController()
        list = userController.getUserInfo(customerName)

        src = {}
        to = {}
        fee = {}
        first = True
        for i in range(3,list.__len__()):
            print("i=", i, ",item=", list.__getitem__(i).__getattribute__("id"))
            idStr = list.__getitem__(i).__getattribute__("id")

            if i % 3 == 0:
                src = {}
                to = {}
                fee={}
            if i%3==0:
                src = list.__getitem__(i)
            if i%3==1:
                to = list.__getitem__(i)
            if i%3==2:
                fee = list.__getitem__(i)
            if (to != {} and src!= {} and fee!={}):
                print(i, ",src=", src.__getattribute__("id"), "to", to.__getattribute__("id"), ",i=", i)
                userAsset = UserAsset.UserAsset()
                userAssetArray = userController.findAssetId(src)
                assetAddressArray = ""
                money = 0
                for each in userAssetArray:
                    money = int(money) + each.money
                    if first==True:
                        assetAddressArray = assetAddressArray + each.assetAddress
                        first= False
                    elif first==False:
                        assetAddressArray = assetAddressArray +","+ each.assetAddress
                transferObject = TransferObject.TransferObject()
                transferObject.srcAccount = src.address
                transferObject.dstAccount = to.address
                if fee!={}:
                     transferObject.feeAccount = fee.address
                transferObject.amount = amount
                if feeAmount!="":
                    transferObject.feeAmount = feeAmount
                transferObject.srcAsset = assetAddressArray
                transferObject.userPrivateKey = src.privateKey
                userController = UserController.UserController()
                src_money = money
                userController.transfer(src, to, fee, src_money, transferObject)

    except Exception as e:
        e = e.with_traceback()
        print(e)
eachTransferToOther("演示环境账本",1,1)