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
from PyQt5.QtCore import QDate,QTimer


from sys import exit,argv

from datetime import datetime,timedelta
from  json import dumps,loads
from requests import post
from configparser import ConfigParser

import sqlexec
import log
import untitled
import datalogic

import common as gl
#global win_main
#global obj1

gl._init()

class ControlBoard(QMainWindow, untitled.Ui_MainWindow):

    def __init__(self, parent=None):
        super(ControlBoard, self).__init__()
        self.setupUi(self)

        self.dateEdit.setDate(QDate.currentDate().addDays(-3))
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("post-api", "post-api"))
        self.setWindowIcon(QtGui.QIcon("F:/temp/pycharm/untitled5/app.ico"))


        self.pushButton.clicked[bool].connect(self.manual)
        self.pushButton_2.clicked[bool].connect(self.on_clicked_button_2)
        self.pushButton_3.clicked[bool].connect(self.on_clicked_button_3)
        #self.textEdit.textChanged.connect(self.del_textbrowser)
        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.del_textbrowser)  # 计时结束调用operate()方法
        self.timer.start(60000)  # 设置计时间隔并启动
    def manual(self):

        execdate= self.dateEdit.date().toString('yyyy.MM.dd ')
        obj1 = Signal()
        gl.set_value('siganl', obj1)
        datalogic.post_data().GetLocalData(execdate)



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

        self.mbt = 线程()
        self.mbt.start()

        self.label_2.setText('定时启动正在执行中,每秒执行一次>>>>> ')


        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(True)


    def on_clicked_button_3(self):
        gl.set_value('是否执行', False)

        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(False)
        self.label_2.setText('定时已经关闭 ')

    def del_textbrowser(self):

        count = gl.get_value('count')
        print("第一次:" + str(count))
        if count > 100:
            self.textBrowser.clear()
            gl.set_value('count',0)



    def outputWritten(self, text):

        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)

        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

class 线程(QtCore.QThread):

    def __init__(self):
        super(线程, self).__init__()
    def run(self,):

         obj1 = Signal()
         gl.set_value('siganl', obj1)
         #ws = weakref.WeakSet()
         #ws.add(obj1)
         obj1.written(str(datetime.now()), "开始")
         print("开启线程")
         datalogic.事务管理().定时执行()

#槽
class QTypeSlot(QtCore.QObject):
    def __init__(self):
        super(QTypeSlot, self).__init__()

    #todo 优化 多个参数
    def get( self,msg1,msg2):
        print("QSlot get msg => " + msg1+' '+msg2)
        global win_main

        win_main.outputWritten(msg1+"----"+msg2+"\n")
        count=gl.get_value('count')
        gl.set_value('count', count+1)


#发射信息
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
        print("进入对话")

        send = QTypeSignal()
        solt = QTypeSlot()
        send.sendmsg.connect(solt.get)
        send.run(str1,str2)

if __name__=='__main__':
    app = QApplication(argv)
    win_main = ControlBoard()
    gl.set_value('win_main', win_main)
    gl.set_value('count', 0)
    win_main.show()
    exit(app.exec_())
