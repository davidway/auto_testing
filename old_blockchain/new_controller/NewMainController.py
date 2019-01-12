# encoding=#utf-8
from new_controller import NewUserController
from new_controller import NewConfigController
from model import UserAsset
from model import NewTransferObject
from model import NewSettleObject
from model import UserInfo
import json
import time
###SQL准备
"""

UPDATE user set id= left(concat(id,MD5(CURRENT_TIMESTAMP) ),12),name =  left(concat(name,MD5(CURRENT_TIMESTAMP) ),12);

delete from user_info;
insert into user_info(userId,customerName) select `user`.id,config.customerName from user,config;
"""


def setConfig(customerName,isTest):
    configController = NewConfigController.NewConfigController()
    config = configController.set(customerName,isTest)
    config.customerName = customerName
    if (config.host == ''):
        raise RuntimeError("设置报文出错了")
    return config
def userReigstUnit(customerName,isTest):
    config = setConfig(customerName,isTest)
    userController = NewUserController.NewUserController()
    userController.createUserList(config)

def issueTest(bossAccount,amount):

    userController = NewUserController.NewUserController()
    userController.issue(bossAccount, amount)
    pass

def transferToAllTest(customerName,isTest,array,amount,feeAmount):
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
                transferObject.srcAccountPublicKey = src.publicKey
                transferObject.srcAccountUid = src.id

                transferObject.dstAccount = to.address
                transferObject.dstAccountPublicKey = to.publicKey
                transferObject.dstAccountUid = to.id

                transferObject.feeAccountPublicKey = fee.publicKey
                transferObject.feeAccount = fee.address
                transferObject.feeAccountUid = fee.id

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
    transferObject.srcAccountPublicKey = src.publicKey
    transferObject.srcAccountUid = src.id

    transferObject.dstAccount = to.address
    transferObject.dstAccountPublicKey = to.publicKey
    transferObject.dstAccountUid = to.id

    transferObject.feeAccountPublicKey = fee.publicKey
    transferObject.feeAccount = fee.address
    transferObject.feeAccountUid = fee.id

    transferObject.amount = amount
    transferObject.feeAmount = feeAmount
    transferObject.srcAsset = assetAddressArray
    transferObject.userPrivateKey = src.privateKey
    userController = NewUserController.NewUserController()
    src_money = money
    userController.transfer(src, to, fee, src_money, transferObject)




def eachTransferToOther(customerName,isTest,array,amount,feeAmount,settleMoney):
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
                transferObject.srcAccountUid = src.id
                transferObject.srcAccountPublicKey = src.publicKey

                transferObject.dstAccount = to.address
                transferObject.dstAccountUid = to.id
                transferObject.dstAccountPublicKey = to.publicKey

                if fee!={}:
                    transferObject.feeAccount = fee.address
                    transferObject.feeAccountUid = fee.id
                    transferObject.feeAccountPublicKey = fee.publicKey
                transferObject.amount = amount
                if feeAmount!="":
                    transferObject.feeAmount = feeAmount
                transferObject.srcAsset = assetAddressArray
                transferObject.userPrivateKey = src.privateKey
                userController = NewUserController.NewUserController()
                src_money = money
                userController.transfer(src, to, fee, src_money, transferObject)

        userController.checkAccount(list,isTest)
    except Exception as e:
        e = e.with_traceback()
        print(e)
def eachSettleTest(array,amount):
    try:
        userController = NewUserController.NewUserController()
        list = userController.getUserInfo(customerName)

        for each in array:
            first = True
            userInfo = list.get(each)
            newSettleObject = NewSettleObject.NewSettleObject()
            newSettleObject.ownerAccount = userInfo.address
            newSettleObject.amount = amount

            userInfo = userController.findUserInfoByAddress(newSettleObject.ownerAccount)

            newSettleObject.userPrivateKey = userInfo.privateKey
            newSettleObject.ownerPublickey = userInfo.publicKey
            newSettleObject.ownerId = userInfo.id

            userAssetArray = userController.findAssetId(userInfo)
            userAssetStr = ""
            first = True
            for each in userAssetArray:
                if first:
                    userAssetStr = userAssetStr + each.assetAddress
                    first = False
                else:
                    userAssetStr = userAssetStr + "," + each.assetAddress
            newSettleObject.srcAsset = userAssetStr
            userController.settle(newSettleObject)

        userController.checkAccount(list,isTest)
    except Exception as e:
        e = e.with_traceback()
        print(e)

def issueUnit(customerName,isTest):
    setConfig(customerName,isTest)
    userController = NewUserController.NewUserController()
    list = userController.getUserInfo(customerName)
    bossAccount = userController.getBossAccount(customerName)
    issueTest(bossAccount,1000000000,customerName)

def accountCheck(customerName,isTest):
    setConfig(customerName,isTest)
    userController = NewUserController.NewUserController()
    list = userController.getUserInfo(customerName)
    userController.checkAccount(list)


customerName = "演示环境账本"
isTest=1
setConfig(customerName,isTest)
#issueUnit(customerName,isTest)

transferToEachOtherArray = [(0, 1, 2), (1, 0, 2), (2, 3, 4), (3, 2, 4), (4, 5, 6), (5, 4, 6), (6, 7, 8), (7, 6, 8),
                                (8, 9, 7), (9, 8, 7)]
transferToAllArray=[(1,2),(3,4),(5,6),(7,8),(0,1),(8,9)]

#transferToAllTest(customerName,isTest,transferToAllArray,8,8)
eachTransferToOther(customerName,isTest,transferToEachOtherArray,1,1,1)
# settleArray = [0,1,2,3,4,5,6,7,8,9]
# settleAmount = 1
# eachSettleTest(settleArray,settleAmount)
