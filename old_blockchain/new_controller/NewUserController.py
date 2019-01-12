from service import NewUserService
import time
from model import UserAsset
from model import UserInfo
from new_controller import NewConfigController
from service import NewUserService
from model import NewTransferObject
from mylog import Log
from model import NewSettleObject

newUserControllerLog = Log.setup_logger("newUserControlelr","newUserController.log")

class NewUserController:

    def setConfig(self,customerName):
        configController = NewConfigController.NewConfigController()
        config = configController.set(customerName,1)
        config.customerName = customerName
        if (config.host == ''):
            raise RuntimeError("设置报文出错了")
        return config

    def getBossAccount(self,customerName):
        newUserService = NewUserService.NewUserService()
        array = []
        array = newUserService.getBossAccount(customerName)
        return array

    def findUserInfoByAddress(self,address):
        newUserService = NewUserService.NewUserService()
        array = []
        user = newUserService.findUserInfoByAddress(address)
        return user


    def getUserInfo(self,customerName):
        newUserService = NewUserService.NewUserService()
        array = []
        array = newUserService.findUserInfo(customerName)
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
                    print(e.with_traceback())
                    array.append(obj)
            return array
        except Exception as e:
            print(e.with_traceback())

    def baasCreateUser(self, id, name):
        newUserService = NewUserService.NewUserService()
        userInfo = newUserService.bassCreateUser(name, id)
        return userInfo

    def updateUserInfo(self, userInfo, userId, customerName):
        newUserService = NewUserService.NewUserService()
        userInfo.userId = userId
        userInfo.customerName = customerName
        newUserService.updateUserInfo(userInfo)
    def issue(self,bossAccount,amount):
        newUserService = NewUserService.NewUserService()
        userAsset = newUserService.issue(bossAccount,amount)
        userAsset = newUserService.insertUserAsset(userAsset)
        return userAsset

    def transfer(self,src,to,fee,srcmoney,transferObject):
        newUserService = NewUserService.NewUserService()
        money = srcmoney
        amount = transferObject.amount

        feeAmount = transferObject.feeAmount
        print("transObject=",transferObject)
        newSrc,newTo,newFee = newUserService.transfer(transferObject)
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
        newUserService.updateAsset(srcAsset)
        newUserService.insertUserAsset(newSrc)
        newUserService.updateAsset(toAsset)
        newUserService.insertUserAsset(newTo)
        if  fee!={}:
            newUserService.updateAsset(feeAsset)
        newUserService.insertUserAsset(newFee)

    def settle(self,settleObject):
        newUserService = NewUserService.NewUserService()
        orgSrc = UserAsset.UserAsset()
        orgSrc.assetAddress = settleObject.srcAsset
        orgSrc.userAddress = settleObject.ownerAccount


        newSrc = newUserService.settle(settleObject)
        newSrc.money = -settleObject.amount
        orgSrc.status=1
        newUserService.updateAsset(orgSrc)
        newUserService.insertUserAsset(newSrc)

    def findAssetId(self,srcAccount):

        userInfo = srcAccount
        newUserService = NewUserService.NewUserService()
        userAssetArray = newUserService.findAssetId(userInfo.address)

        return userAssetArray

    def checkAccount(self,list):
        newUserService = NewUserService.NewUserService()
        for each in list:
            sqlAccountCheck = newUserService.getUserAccountFromSql(each)
            userAccountBaas = newUserService.getUserAccountFromBass(each)
            assert (sqlAccountCheck.money == userAccountBaas.money), "不正确，请查看资产地址："+each.address+",sqlAccountCheck.money="+str(sqlAccountCheck.money)+",userAccountBaas.money="+str(userAccountBaas.money)
            assert (sqlAccountCheck.assetAddress == userAccountBaas.assetAddress), "不正确，请查看资产地址："+each.address+",sqlAccountCheck.assetAddress="+sqlAccountCheck.assetAddress+",userAccountBaas.assetAddress="+userAccountBaas.assetAddress

