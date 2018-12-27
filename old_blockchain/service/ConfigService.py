# -*- coding: UTF-8 -*-

import json

from dao import ConfigDao
from model import Config
import requests
import time


def safeRequests(url,data,headers,cookies):
    result=""
    tryTimes=0
    while tryTimes<=3:
        try:
            result = requests.post(url,data=data,headers=headers,cookies=cookies)
            print(result)
            return result
        except Exception as e:
            print(e)
            time.sleep(2)
            tryTimes= tryTimes+1


def baasSetConfig(customerName):
    headers = {
        'Accept': "application/json",
        'Content-Type': "application/json;charset=UTF-8"
    }



    # 字典转化为json
    try:
        config = Config.Config()
        config.customerName = customerName
        configDao = ConfigDao.ConfigDao()
        config = configDao.get(config)

        config = config.__dict__
        configJson = json.dumps(config)

        # 打印字典
        print(config)
        url = 'http://localhost:8080/blockchain/configProperties/add'
        data = configJson
        headers = headers
        result = safeRequests(url, data, headers,"")


        if result.status_code == 200:
            jsonResult = result.json()

            if ( jsonResult['retcode']!=0):
                raise Exception("请求错误，请查看信息:",jsonResult)
            if jsonResult['data']!='':
                return jsonResult['data']
        else:
            print( Exception("错误信息",result.json()))
    except Exception as e:
        print(e)

class ConfigService:
    def setByCustomerName(self,customerName):

        config = baasSetConfig(customerName)
        return config



