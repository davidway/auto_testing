from service import UserService
import time
from model import UserAsset
from model import UserInfo
class UserController:

    def getBossAccount(self,customerName):
        userService = UserService.UserService()
        array = []
        array = userService.getBossAccount(customerName)
        return array

    def findUserInfoByAddress(self,address):
        userService = UserService.UserService()
        array = []
        user = userService.findUserInfoByAddress(address)
        return user


    def getUserInfo(self,customerName):
        userService = UserService.UserService()
        array = []
        array = userService.findUserInfo(customerName)
        return array

    def createUserList(self,config):
        array = []
        try:
            bossAccount = {}
            array = self.getUserInfo(config.customerName)
            for obj in array:
                try:
                    userInfo =  self.baasCreateUser(obj.id, obj.name)

                    self.updateUserInfo(userInfo, obj.id, config.customerName)
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
        userAsset = userService.issue(bossAccount,amount)
        userAsset = userService.insertUserAsset(userAsset)
        return userAsset

    def transfer(self,src,to,fee,srcmoney,transferObject):
        userService = UserService.UserService()
        money = srcmoney
        amount = transferObject.amount

        feeAmount = transferObject.feeAmount
        print("transObject=",transferObject)
        newSrc,newTo,newFee = userService.transfer(transferObject)
        srcAsset = UserAsset.UserAsset()
        toAsset = UserAsset.UserAsset()
        feeAsset = UserAsset.UserAsset()

        srcAsset.status = 1
        srcAsset.userAddress = transferObject.srcAccount
        srcAsset.assetAddress = transferObject.srcAsset

        toAsset.userAddress = transferObject.dstAccount
        toAsset.assetAddress=""
        toAsset.money=0
        if fee!={}:
            feeAsset.userAddress = transferObject.feeAccount
            feeAsset.assetAddress=""
            feeAsset.money=0
        if feeAmount!="":
            newSrc.money = -amount-feeAmount
        else:
            newSrc.money = -amount
        to.status=1
        to.money = amount
        if  fee!={}:
            fee.status=1
            fee.money = feeAmount
        userService.updateAsset(srcAsset)
        userService.insertUserAsset(newSrc)
        userService.updateAsset(toAsset)
        userService.insertUserAsset(newTo)
        if  fee!={}:
             userService.updateAsset(feeAsset)
        userService.insertUserAsset(newFee)

    def settle(self,settleObject):
        userService = UserService.UserService()
        orgSrc = UserAsset.UserAsset()
        orgSrc.assetAddress = settleObject.srcAsset
        orgSrc.userAddress = settleObject.ownerAccount


        newSrc = userService.settle(settleObject)
        newSrc.money = -settleObject.amount
        orgSrc.status=1
        userService.updateAsset(orgSrc)
        userService.insertUserAsset(newSrc)

    def findAssetId(self,srcAccount):

        userInfo = srcAccount
        userService = UserService.UserService()
        userAssetArray = userService.findAssetId(userInfo.address)

        return userAssetArray


