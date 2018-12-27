# encoding=#utf-8
from controller import UserController
from controller import ConfigController

def setConfig(customerName):
    configController = ConfigController.ConfigController()
    config = configController.set(customerName)
    if (config.ledgerId == ''):
        raise RuntimeError("设置报文出错了")
def createUser():
    userController = UserController.UserController()
    try:
        array = userController.getUserInfo()
        for obj in array:
           userController.baasCreateUser(obj.id,obj.name)
    except Exception as e:
        print(e)
def issue():
    pass
def transfer(src,to,account):
    pass
def settle(src,account):
    pass
setConfig("自己测试用的")
createUser()

