# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from configparser import ConfigParser
from  json import dumps,loads
from gc import collect
from requests import post
from time import sleep
from datetime import datetime,timedelta

import sqlexec
import log
import common as gl


class post_data():

    def GetLocalData(self,date):

        try:

            try:
                sqlexec.SQLServer().execccgc(date)
            except Exception:
               pass

            dt=sqlexec.SQLServer.excqurey("select flowno,posno,memo,cardcode,payamount,transdate from Zicsale where send='0'", ["flowno", "posno", "memo", "cardcode", "payamount", "transdate"])
            print("本地信息获取成功")

            count=str(len(dt))
            if len(dt)>0:
                cp = ConfigParser()
                cp.read("db.cfg",encoding="utf-8-sig")
                section = cp.sections()[0]
                shopname = cp.get(section, "shop")
                print(shopname)
                dict ={'value':dt}
                dt=None
                #va_name = sqlexec.SQLServer.excqurey("select englishname from system", ["englishname"])
                #shopname=va_name[0]["englishname"]
                dict["ShopName"] = shopname
                url = cp.get(section, "url")
                js = dumps(dict)

                data = js
                #提交数据
                response = post(url, data=data)
                print(loads(response.content))
                if loads(response.content)["code"]==100:
                   sqlexec.SQLServer().Exec("delete from Zicsale where transdate< dateadd(day,-20,getdate())   ")
                   sqlexec.SQLServer().Exec(" update Zicsale set send='1'")

                   vs="服务器反馈提交成功"+count+"记录"
            else:
                vs = "无需提交没有新记录"

            log.get_logger().info(vs)
            win_main1 = gl.get_value('win_main')

            siganl = gl.get_value('siganl')
            siganl.written(str(datetime.now()), vs)

            return vs
        except Exception as e:
            log.get_logger().error(str(e))
        finally:
            return

class 事务管理():
    def 定时执行(self):
        gl.set_value('是否执行', True)
        是否执行=True
        print("是否执行")
        cp = ConfigParser()
        cp.read("db.cfg")
        section = cp.sections()[0]
        times=cp.getint(section, "time")
        while gl.get_value('是否执行')==True:
             print("事务开始")
             now = datetime.now()
             delta = timedelta(days=-3)
             n_days = now + delta
             datetime_p=datetime.strftime(n_days,'%Y.%m.%d ')
             post_data().GetLocalData(str(datetime_p))
             sleep(times)

