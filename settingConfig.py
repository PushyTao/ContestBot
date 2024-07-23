import json


def settingNumber():
    """
    通过读取配置文件的内容设置账号和群号
    :return: {'user':登陆的用户名,'sendGroupNumber':需要每日播报的群,
               'monitorGroupNumber':监视的群,'autoSendTime':每日播报的时间}
    """
    with open('./config.json') as j:
        cfg = json.load(j)
        cfgUser = cfg['userNumber']
    return cfgUser


def settingPost():
    """
    通过json文件配置端口的信息
    :return: {'host':需要监听的程序的地址,'port':监听的端口}
    """
    with open('./config.json') as j:
        cfg = json.load(j)
        cfgPost = cfg['POST']
    return cfgPost


def settingDb():
    with open('./config.json') as j:
        cfg = json.load(j)
        cfgDb = cfg['SQLINFO']
    return cfgDb
