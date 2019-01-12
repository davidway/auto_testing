from service import NewConfigService
from model import NewConfig
import json
class NewConfigController:
    def set(self,customerName,isTest):
        configService = NewConfigService.NewConfigService()
        configDict = configService.setNewBassByCustomerName(customerName,isTest)

        config = NewConfig.NewConfig()

        config.createUserPublicKey = configDict['createUserPublicKey']
        config.createUserPrivateKey = configDict['createUserPrivateKey']
        config.chainId = configDict['chainId']
        config.mchId = configDict['mchId']
        config.nodeId = configDict['nodeId']
        config.host = configDict['host']

        return config


