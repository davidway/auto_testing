# encoding=#utf-8

from pymysql import connect
from dao import BaseDao

from model import Config
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
            result = baseDao.executeSql(sql, param)
            result = result[0]
            config = Config.Config()
            config.createUserPrivateKey,config.createUserPublicKey,config.mchId,config.chainId,config.ledgerId,config.nodeId=result
            return config
        except Exception as e:
            print(e)
