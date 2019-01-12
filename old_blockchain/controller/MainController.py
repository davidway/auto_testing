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
    configController = NewConfigController.NewConfigController()
    config = configController.set(customerName)
    config.customerName = customerName
    if (config.ledgerId == ''):
        raise RuntimeError("设置报文出错了")
    return config
def userReigstUnit(customerName):
    config = setConfig(customerName)
    userController = NewUserController.NewUserController()
    userController.createUserList(config)

def issueTest(bossAccount,amount,customerName):

    userController = NewUserController.NewUserController()
    userController.issue(bossAccount, amount)
    pass

def transferToAllTest(customerName,array,amount,feeAmount):
    try:
        userController = NewUserController.NewUserController()
        list = userController.getUserInfo(customerName)

        src = userController.getBossAccount( customerName)
        for each in array:
            to = list.__getitem__(each[0])
            fee =  list.__getitem__(each[1])
            if (to != {} and fee != {}):

                userAsset = UserAsset.UserAsset()
                userAssetArray = userController.findAssetId(src)
                assetAddressArray = ""
                money = 0
                for each in userAssetArray:
                    money = int(money) + each.money
                    assetAddressArray = assetAddressArray + each.assetAddress
                transferObject = NewTransferObject.NewTransferObject()
                transferObject.srcAccount = src.address
                transferObject.dstAccount = to.address
                transferObject.feeAccount = fee.address
                transferObject.amount = amount
                transferObject.feeAmount = feeAmount
                transferObject.srcAsset = assetAddressArray
                transferObject.userPrivateKey = src.privateKey
                userController = NewUserController.NewUserController()
                src_money = money
                userController.transfer(src, to, fee, src_money, transferObject)
        userController.checkAccount(list)
    except Exception as e:
        print(e)
def settleTest(address,amount):
    userController = NewUserController.NewUserController()
    userInfo = UserInfo.UserInfo()

    list=[]
    settleObject =NewSettleObject.NewSettleObject()
    settleObject.amount = amount
    settleObject.ownerAccount = address

    userInfo = userController.findUserInfoByAddress(settleObject.ownerAccount)
    list.append(userInfo)
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
    userController = NewUserController.NewUserController()
    userAsset = UserAsset.UserAsset()
    userAssetArray = userController.findAssetId(src)
    assetAddressArray = ""
    money = 0
    for each in userAssetArray:
        money = int(money) + each.money
        assetAddressArray = assetAddressArray + each.assetAddress
    transferObject = NewTransferObject.NewTransferObject()
    transferObject.srcAccount = src.address
    transferObject.dstAccount = to.address
    transferObject.feeAccount = fee.address
    transferObject.amount = amount
    transferObject.feeAmount = feeAmount
    transferObject.srcAsset = assetAddressArray
    transferObject.userPrivateKey = src.privateKey
    userController = NewUserController.NewUserController()
    src_money = money
    userController.transfer(src, to, fee, src_money, transferObject)




def eachTransferToOther(customerName,array,amount,feeAmount):
    try:
        userController = NewUserController.NewUserController()
        list = userController.getUserInfo(customerName)
        src = {}
        to = {}
        fee = {}
        first = True
        for each in array:
            first = True
            src =list.__getitem__(each[0])
            to =list.__getitem__(each[1])
            fee =list.__getitem__(each[2])
            if (to != {} and src!= {} and fee!={}):
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
                transferObject = NewTransferObject.NewTransferObject()
                transferObject.srcAccount = src.address
                transferObject.dstAccount = to.address
                if fee!={}:
                     transferObject.feeAccount = fee.address
                transferObject.amount = amount
                if feeAmount!="":
                    transferObject.feeAmount = feeAmount
                transferObject.srcAsset = assetAddressArray
                transferObject.userPrivateKey = src.privateKey
                userController = NewUserController.NewUserController()
                src_money = money
                userController.transfer(src, to, fee, src_money, transferObject)
                settleTest(src.address,1)
                settleTest(to.address, 1)
                settleTest(fee.address, 1)
        userController.checkAccount(list)
    except Exception as e:
        e = e.with_traceback()
        print(e)


def issueUnit(customerName):
    bossAccount = {}
    setConfig(customerName)
    userController = NewUserController.NewUserController()
    list = userController.getUserInfo(customerName)
    bossAccount = userController.getBossAccount(customerName)
    issueTest(bossAccount,1000000000,customerName)

def accountCheck(customerName):
    setConfig(customerName)
    userController = NewUserController.NewUserController()
    list = userController.getUserInfo(customerName)
    userController.checkAccount(list)


customerName = "土豆链"
issueUnit(customerName)

transferToEachOtherArray = [(0, 1, 2), (1, 0, 2), (2, 3, 4), (3, 2, 4), (4, 5, 6), (5, 4, 6), (6, 7, 8), (7, 6, 8),
                                (8, 9, 7), (9, 8, 7)]
transferToAllArray=[(1,2),(3,4),(5,6),(7,8),(0,1),(8,9)]

transferToAllTest(customerName,transferToAllArray,8,8)
eachTransferToOther(customerName,transferToEachOtherArray,1,1)

