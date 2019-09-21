# _*_ codeing:utf-8 _*_
# 开发团队:福州通和
# 开发人员:zengl
#开发时间:2019-06-2415:50 
#文件名称:data_post


import pymssql
from datetime import datetime
from decimal import *
from configparser import ConfigParser



from log import get_logger





class SQLServer:
    def __init__(self):
        # 类的构造函数，初始化DBC连接信息
        cp = ConfigParser()
        cp.read("db.cfg")
        section = cp.sections()[0]

        self.server=cp.get(section, "host")+":"+cp.get(section, "port")
        self.user = cp.get(section, "user")
        self.password = '1The2quick3brown4fox5jumps6ove'
        self.database = cp.get(section, "db")

    def __getconnect(self):
        if not self.database:
            get_logger().error("没有设置数据库信息" )
            raise (NameError, "没有设置数据库信息")

        print(self.server+self.user+self.password +self.database)
        self.conn = pymssql.connect(server=self.server, user=self.user, password=self.password, database=self.database)
        cur = self.conn.cursor()
        print("shujuklj")
        if not cur:
            get_logger().error("连接数据库失败" + self.conn )
            raise (NameError, "连接数据库失败")  # 将DBC信息赋值给cur
        else:
            return cur

    def ExecQuery(self, sql):
        try:
            cur = self.__getconnect()

            cur.execute(sql)
            result = cur.fetchall()
            self.conn.commit()
            self.conn.close()
            return result
        except Exception as e:
            get_logger().error("语句" + str(e))
            raise
    def Exec(self, sql):
        try:
            cur = self.__getconnect()
            print("执行语句"+sql)
            cur.execute(sql)
            get_logger().info("执行语句" + sql+"成功")

            self.conn.commit()
            self.conn.close()

        except Exception as e:
            get_logger().error("语句" + str(e))
            raise


    def execccgc(self,date):
            cons=self.__getconnect()

            cons.callproc("ZICSALELS ",(date,))
            self.conn.commit()

            print("执行的开始时间" + date)


    def excqurey(sql, parms):
            jsondata = []
            curr = SQLServer()
            result = curr.ExecQuery(sql)

            for row in result:
                result_1 = {}
                i = 0
                for parm in parms:
                    detail_data = row[i]
                    if (isinstance(detail_data, Decimal)):
                        #####################Decimal转换成文本
                        result_1[parm] = str(row[i])
                    elif (isinstance(detail_data, datetime)):
                        ########################日期型数据转换成可读模式
                        result_1[parm] = row[i].strftime('%Y.%m.%d %H:%M:%S')
                    else:
                        result_1[parm] = row[i]
                    i = i + 1
                jsondata.append(result_1)
            # jsondatar = json.dumps(jsondata, ensure_ascii=False)
            return jsondata








#resposen =requests.request('POST','http://192.168.31.110:5000/icsend',data='223434345')
#print(resposen.content)
if __name__ == '__main__':
   SQLServer().execccgc()


