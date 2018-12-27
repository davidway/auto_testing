from service import ConfigService
from model import Config
import json
class ConfigController:
    def set(self,customerName):
        configService = ConfigService.ConfigService()
        configDict = configService.setByCustomerName(customerName)
        configJson = json.dumps(configDict)

        config = Config.Config()
        config.__dict__  = dict
        return config


