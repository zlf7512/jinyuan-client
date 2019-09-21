# _*_ codeing:utf-8 _*_
# 开发团队:福州通和
# 开发人员:zengl
#开发时间:2019-07-0516:17 
#文件名称:common
def _init():
    global _global_dict
    _global_dict = {}

def set_value(name, value):
    _global_dict[name] = value

def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue