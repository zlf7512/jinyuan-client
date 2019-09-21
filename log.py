#！/usr/bin/env python
#_*_coding:utf-8_*_
#@author :yinzhengjie
#blog:http://www.cnblogs.com/yinzhengjie/tag/python%E8%87%AA%E5%8A%A8%E5%8C%96%E8%BF%90%E7%BB%B4%E4%B9%8B%E8%B7%AF/
#EMAIL:y1053419035@qq.com


from logging import  getLogger,INFO,StreamHandler,basicConfig,CRITICAL,FileHandler,Formatter
from datetime import datetime
from os import path,mkdir

'''
Python使用logging模块记录日志涉及四个主要类，使用官方文档中的概括最为合适：
    1>.logger提供了应用程序可以直接使用的接口；
    2>.handler将(logger创建的)日志记录发送到合适的目的输出；
    3>.filter提供了细度设备来决定输出哪条日志记录；
    4>.formatter决定日志记录的最终输出格式。
'''

def get_logger():
    logger_obj = getLogger()                        #创建一个logger对象，它提供了应用程序可以直接使用的接口，其类型为“<class 'logging.RootLogger'>”；
    basicConfig(level=INFO)
    isExists = path.exists("log")
    if not isExists:
      mkdir("log")
    fh = FileHandler("log\\log"+datetime.now().date().isoformat()+".txt")          #创建一个文件输出流；
    fh.setLevel(INFO)                              #定义文件输出流的告警级别；

    ch = StreamHandler()                           #创建一个屏幕输出流；
    ch.setLevel(CRITICAL)                           #定义屏幕输出流的告警级别；

    formater = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')        #自定义日志的输出格式，这个格式可以被文件输出流和屏幕输出流调用；
    fh.setFormatter(formater)                                #添加格式花输出，即调用我们上面所定义的格式，换句话说就是给这个handler选择一个格式；
    ch.setFormatter(formater)

    logger_obj.addHandler(fh)                               #logger对象可以创建多个文件输出流（fh）和屏幕输出流（ch）哟
    logger_obj.addHandler(ch)


    return logger_obj                                      #将我们创建好的logger对象返回

if __name__ == '__main__':
     get_logger().info("qqqq")


