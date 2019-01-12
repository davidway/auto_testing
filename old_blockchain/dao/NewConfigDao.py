# encoding=#utf-8

from dao import BaseDao
import json

from model import NewConfig
from model import GLOBAL_CONFIG
globalConfig = GLOBAL_CONFIG.GLOBAL_CONFIG()
host = globalConfig.host

class NewConfigDao(BaseDao.BaseDao):
    def get(self, newConfig):
        if newConfig.customerName=="":
            raise RuntimeError('出错了')

        sql = """
select createUserPrivateKey,createUserPublicKey,mchId,chainId,nodeId,host from new_config where customerName=%s and isTest=%s
        """
        param = []
        param.append(newConfig.customerName)
        param.append(newConfig.isTest)
        try:
            baseDao = BaseDao.BaseDao()
            result = baseDao.executeGetAllSql(sql, param)
            result = result[0]
            newConfig = NewConfig.NewConfig()
            newConfig.createUserPrivateKey,newConfig.createUserPublicKey,newConfig.mchId,newConfig.chainId,newConfig.nodeId,newConfig.host=result
            return newConfig
        except Exception as e:
            print(e)

    def baasSetConfig(self,customerName):
        headers = {
            'Accept': "application/json",
            'Content-Type': "application/json;charset=UTF-8"
        }
        # 字典转化为json
        try:
            baseDao = BaseDao.BaseDao()

            newConfig = NewConfig.NewConfig()
            newConfig.customerName = customerName
            newConfigDao = NewConfigDao()
            newConfig = newConfigDao.get(newConfig)

            newConfig = newConfig.__dict__
            configJson = json.dumps(newConfig)

            # 打印字典
            print(config)
            url = host+'configProperties/add'
            data = configJson
            headers = headers
            result =baseDao.safeRequests(url, data, headers,"")


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

    def setNewBassByCustomerName(self,customerName,isTest):
        headers = {
            'Accept': "application/json",
            'Content-Type': "application/json;charset=UTF-8"
        }
        # 字典转化为json
        try:
            baseDao = BaseDao.BaseDao()

            newConfig = NewConfig.NewConfig()
            newConfig.customerName = customerName
            newConfig.isTest= isTest
            configDao = NewConfigDao()
            config = configDao.get(newConfig)

            config = config.__dict__
            configJson = json.dumps(config)

            # 打印字典
            print(config)
            url = host + 'configProperties/add'
            data = configJson
            headers = headers
            result = baseDao.safeRequests(url, data, headers, "")

            if result.status_code == 200:
                jsonResult = result.json()

                if (jsonResult['retcode'] != 0):
                    raise Exception("请求错误，请查看信息:", jsonResult)
                if jsonResult['data'] != '':
                    return jsonResult['data']
            else:
                print(Exception("错误信息", result.json()))
        except Exception as e:
            print(e)
