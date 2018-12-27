# encoding=#utf-8
from controller import UserController
from controller import ConfigController
import time

def setConfig(customerName):
    configController = ConfigController.ConfigController()
    config = configController.set(customerName)
    config.customerName = customerName
    if (config.ledgerId == ''):
        raise RuntimeError("设置报文出错了")
    return config



###SQL准备
"""

UPDATE user set id= left(concat(id,MD5(CURRENT_TIMESTAMP) ),12),name =  left(concat(name,MD5(CURRENT_TIMESTAMP) ),12);

delete from user_info;
insert into user_info(userId,customerName) select `user`.id,config.customerName from user,config;
"""
def configUnit():
    config = setConfig("自己测试用的")
def userReigstUnit():
    config = setConfig("自己测试用的")
    userController = UserController.UserController()
    userController.createUserList(config)

def issueUnit():
    userController = UserController.UserController()
    list = userController.getUserInfo("自己测试用的")

    bossAccount = userController.getBossAccount(list)
    userAsset = userController.issue(bossAccount, 10000)

def transferUnit():
    pass
def mulitiTransferUnit():
    pass

def settleUnit():
    pass


configUnit()
userReigstUnit()
issueUnit()
transferUnit()



