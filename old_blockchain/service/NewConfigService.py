# -*- coding: UTF-8 -*-

import json

from dao import NewConfigDao
from model import NewConfig
import requests
import time




class NewConfigService:

    def setNewBassByCustomerName(self,customerName,isTest):
        configDao = NewConfigDao.NewConfigDao()
        config = configDao.setNewBassByCustomerName(customerName,isTest)
        return config


