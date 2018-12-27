from service import UserService

class UserController:
    def getUserInfo(self):
        userService = UserService.UserService()
        array = []
        array = userService.findUserInfo()
        return array

    def baasCreateUser(self, id, name):
        userService = UserService.UserService()
        userInfo = userService.bassCreateUser(name, id)
        return userInfo

    def updateUserInfo(self, userInfo, userId, customerName):
        userService = UserService.UserService()
        userInfo.userId = userId
        userInfo.customerName = customerName
        userService.updateUserInfo(userInfo)


