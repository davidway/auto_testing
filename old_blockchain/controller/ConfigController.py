from service import ConfigService
from model import Config

import json
from mylog import Log

configControllerLog = Log.setup_logger('configControllerLog', 'configControllerLog.log')




class ConfigController:
    def set(self,customerName):
        configService = ConfigService.ConfigService()
        configDict = configService.setByCustomerName(customerName)


        config = Config.Config()
        config.ledgerId = configDict['ledgerId']
        config.createUserPublicKey = configDict['createUserPublicKey']
        config.createUserPrivateKey = configDict['createUserPrivateKey']
        config.chainId = configDict['chainId']
        config.mchId = configDict['mchId']
        config.nodeId = configDict['nodeId']

        configControllerLog.debug("config=",config)
        return config


