# encoding=#utf-8

from pymysql import connect
from dao import BaseDao
import json
from model import Config
from model import GLOBAL_CONFIG
globalConfig = GLOBAL_CONFIG.GLOBAL_CONFIG()
host = globalConfig.host

class ConfigDao(BaseDao.BaseDao):
    def get(self, config):
        if config.customerName=="":
            raise RuntimeError('出错了')

        sql = """
            select privateKey,publicKey,mchId,chainId,ledgerId,nodeId from config where customerName=%s
        """
        param = []
        param.append(config.customerName)
        try:
            baseDao = BaseDao.BaseDao()
            result = baseDao.executeGetAllSql(sql, param)
            result = result[0]
            config = Config.Config()
            config.createUserPrivateKey,config.createUserPublicKey,config.mchId,config.chainId,config.ledgerId,config.nodeId=result
            return config
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

            config = Config.Config()
            config.customerName = customerName
            configDao = ConfigDao()
            config = configDao.get(config)

            config = config.__dict__
            configJson = json.dumps(config)

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
