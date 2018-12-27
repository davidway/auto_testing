from service import UserService
import time
class UserController:
    def getUserInfo(self,customerName):
        userService = UserService.UserService()
        array = []
        array = userService.findUserInfo(customerName)
        return array

    def createUserList(self,config):
        array = []

        userController = UserController.UserController()
        try:
            bossAccount = {}
            array = userController.getUserInfo(config.customerName)
            for obj in array:
                try:
                    userInfo = userController.baasCreateUser(obj.id, obj.name)

                    userController.updateUserInfo(userInfo, obj.id, config.customerName)
                    time.sleep(1)

                except Exception as e:
                    print(e)
                    array.append(obj)
            return array
        except Exception as e:
            print(e)

    def baasCreateUser(self, id, name):
        userService = UserService.UserService()
        userInfo = userService.bassCreateUser(name, id)
        return userInfo

    def updateUserInfo(self, userInfo, userId, customerName):
        userService = UserService.UserService()
        userInfo.userId = userId
        userInfo.customerName = customerName
        userService.updateUserInfo(userInfo)
    def issue(self,bossAccount,amount):
        userService = UserService.UserService()
        userAsset = userService.issue(bossAccount,"1000")
        userAsset = userService.insertUserAsset(userAsset)
        return userAsset

    def transfer(self,src,to,fee,amount,feeAmount):
        userService = UserService.UserService()
        src,to,fee = userService.transfer(self,src,to,fee,amount,feeAmount)
        userService.updateAsset(src)
        userService.insertUserAsset(src)
        userService.updateAsset(to)
        userService.insertUserAsset(to)
        userService.updateAsset(fee)
        userService.insertUserAsset(fee)
        pass
    def settle(self,src,account):
        userService = UserService.UserService()
        userService.settle(src, account)
        userService.updateAsset(src)
        userService.insertUserAsset(src)
