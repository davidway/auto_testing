
from pymysql import connect
class BaseDao:

    def executeSql(self,sql, param=""):
        # 查询数据库的方法
        try:
            db = connect(host="localhost",
                         user="root",
                         password="123456",
                         db="old_blockchain",
                         port=3306,
                         charset="utf8")
            # 打开数据库连接
            cur = db.cursor()
            # 使用cursor()方法获取操作游标
            sql = sql
            # sql语句
            if param!="":
                 cur.execute(sql, param)
            else:
                cur.execute(sql)
            # 执行sql语句
            results = cur.fetchall()
            # 获取查询的结果
            db.commit()
            # 提交
            cur.close()
            # 关闭游标
            db.close()
            # 断开数据库连接
            return results
        except Exception as e:
            print(e)
            db.rollback()
        # 返回一个list
        pass
