# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtGui
import weakref
from gc import collect


from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate


from sys import exit,argv

from datetime import datetime,timedelta
from  json import dumps,loads
from requests import post
from configparser import ConfigParser

import sqlexec
import log
import untitled

global win

class QTypeSlot(QtCore.QObject):
    def __init__(self):
        super(QTypeSlot, self).__init__()

    #todo 优化 多个参数
    def get( self,msg1,msg2):
        print("QSlot get msg => " + msg1+' '+msg2)
        global win
        win.outputWritten(msg1+"----"+msg2+"\n")


class QTypeSignal(QtCore.QObject):
    sendmsg = pyqtSignal(str, str)

    def __init__(self):
        super(QTypeSignal, self).__init__()

    def run(self,str1,str2):
        # 发射信号
        # self.sendmsg.emit('hell')
        # todo 优化 发射多个参数
        self.sendmsg.emit(str1,str2)



class Signal():
    def written(self,str1,str2):
        send = QTypeSignal()
        solt = QTypeSlot()
        send.sendmsg.connect(solt.get)
        send.run(str1,str2)


class post_data():

    def click(self,ds):

        try:
            cp = ConfigParser()
            cp.read("db.cfg")
            section = cp.sections()[0]


            sqlexec.SQLServer().execccgc(ds)
            dt=sqlexec.SQLServer.excqurey("select flowno,posno,memo,cardcode,payamount,transdate from Zicsale", ["flowno", "posno", "memo", "cardcode", "payamount", "transdate"])
            count=str(len(dt))
            dict ={'value':dt}
            dt=None
            va_name = sqlexec.SQLServer.excqurey("select englishname from system", ["englishname"])
            shopname=va_name[0]["englishname"]
            dict["ShopName"] = shopname
            url = cp.get(section, "url")
            js = dumps(dict)
            #print(js)
            data = js
            response = post(url, data=data)
            print(loads(response.content))



            vs="服务器反馈提交成功"+count+"记录"
            #log.get_logger().info(vs)
            del data, dt, js, cp, section, dict
            collect()

            return vs

        except Exception as e:
            log.get_logger().error(str(e))
        finally:
            return

class ControlBoard(QMainWindow, untitled.Ui_MainWindow):

    def __init__(self, parent=None):
        super(ControlBoard, self).__init__()
        self.setupUi(self)
        self.timer_id = 0
        self.dateEdit.setDate(QDate.currentDate().addDays(-3))
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("post-api", "post-api"))
        self.setWindowIcon(QtGui.QIcon("F:/temp/pycharm/untitled5/app.ico"))


        self.pushButton.clicked[bool].connect(self.click)
        self.pushButton_2.clicked[bool].connect(self.on_clicked_button_2)
        self.pushButton_3.clicked[bool].connect(self.on_clicked_button_3)

    def closeEvent(self, QCloseEvent):
        res = QMessageBox.question(self, '消息', '是否关闭这个窗口？', QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)  # 两个按钮是否， 默认No则关闭这个提示框
        if res == QMessageBox.Yes:
             QCloseEvent.accept()
        else:
           QCloseEvent.ignore()

    def on_clicked_button_2(self):

        self.dateEdit.setDate(QDate.currentDate().addDays(-3))
        cp = ConfigParser()
        cp.read("db.cfg")
        section = cp.sections()[0]
        time = cp.getfloat(section, "time")
        self.label_2.setText('定时启动正在执行中,每'+str(time)+'秒执行一次>>>>> ')

        self.timer_id = self.startTimer(1000*time, timerType=QtCore.Qt.VeryCoarseTimer)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(True)

    def timerEvent(self, event):
        self.click()
        # self.mbt = MyBeautifulThread()
        # self.mbt.start()
        # self.pushButton.setEnabled(False)

    def on_clicked_button_3(self):
        if self.timer_id:
            self.killTimer(self.timer_id)
            self.timer_id = 0
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(False)
        self.label_2.setText('定时已经关闭 ')

    def click(self):

        try:

            ds = QDate.toString(self.dateEdit.date(), "yyyy.MM.dd")
            obj=post_data()
            ws = weakref.WeakSet()
            ws.add(obj)
            vs = obj.click(ds)
            obj1=Signal()
            ws = weakref.WeakSet()
            ws.add(obj1)
            obj1.written(str(datetime.now()), vs)
            del obj
            del obj1

        except Exception as e:
            log.get_logger().error(str(e))

    def outputWritten(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)

        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

class MyBeautifulThread(QtCore.QThread):

    def __init__(self):
        super(MyBeautifulThread, self).__init__()
    def run(self,):
         global win
         # now = datetime.now()
         # delta = timedelta(days=-3)
         # n_days = now + delta
         # n_days.strftime('%Y.%m.%d ')
         win.click()

if __name__=='__main__':

    app = QApplication(argv)
    global win
    win = ControlBoard()
    win.show()
    exit(app.exec_())



