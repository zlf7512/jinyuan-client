# _*_ codeing:utf-8 _*_
# 开发团队:福州通和
# 开发人员:zengl
#开发时间:2019-07-1916:09 
#文件名称:请求测试

from requests import post
from  json import dumps,loads

class 请求:
    def __init__(self):
       print("ok")
    def 发送(self):
        dict={}
        dict["adc"]="15546"
        print(type(dict))
        js = dumps(dict)
        data = js
        url="http://thx.thsen.top:5000/Postsheet"
        response = post(url, data=data)
        print(loads(response.content))
if __name__=='__main__':
    请求().发送()

