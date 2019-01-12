# -*- coding: UTF-8 -*-

import json

from dao import ConfigDao
from model import Config
import requests
import time




class ConfigService:
    def setByCustomerName(self,customerName):
        configDao = ConfigDao.ConfigDao()
        config = configDao.baasSetConfig(customerName)
        return config




