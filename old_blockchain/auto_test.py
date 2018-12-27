# encoding=#utf-8
from controller import UserController
from controller import ConfigController

def autoScript(customerName):
    configController = ConfigController.ConfigController()
    config = configController.set(customerName)
    if (config.ledgerId == ''):
        raise RuntimeError("设置报文出错了")

    userController = UserController.UserController()
    array = userController.getUserInfo()
    for id, name in array:
       print(id,name)

autoScript("酷哒国际")


