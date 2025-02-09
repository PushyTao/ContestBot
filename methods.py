import os

import contestDBoperate
from atcoder import *
from newcoder import *
from codeforces import *

url_reboot = "http://127.0.0.1:5700"


def sendGroupMessage(group_id, message):
    """
    向群组中发送文字消息
    :param group_id: 群号
    :param message: 文字消息
    :return: null，发送消息
    """
    data = {
        "group_id": group_id,
        "message": message
    }
    requests.post(url=url_reboot + "/send_group_msg", json=data)


def sendPrivateMessage(uid, message):
    """
    向私聊消息中发送文字消息
    :param uid: 对方的qq号
    :param message: 想要给对方发送的消息
    :return: null，发送消息
    """
    data = {
        "user_id": uid,
        "message": message
    }
    requests.post(url=url_reboot + "/send_private_msg", json=data)


def sendGroupContest(type, group_id):
    """
    向群组发送比赛日历
    :param type: 比赛的名称 cf-codeforces，at-atcoder，nk-牛客
    :param group_id: 群号
    :return: null，调用的sendGroupMessage()
    """
    # cf 的比赛信息
    if type == 'cf':
        sendGroupMessage(group_id, message_codeforces_all())
    # atcoder 的比赛信息
    elif type == 'at':
        sendGroupMessage(group_id, message_atcoder_all())
    # 牛客的比赛信息
    elif type == 'nk':
        sendGroupMessage(group_id, message_newcoder_all())


def sendPrivateContest(type, uid):
    """
    向个人的qq发送比赛日历
    :param type: 比赛的名称 cf-codeforces，at-atcoder，nk-牛客
    :param uid: 对方的qq号
    :return: null，调用的sendGroupMessage()
    """
    # cf的比赛信息
    if type == 'cf':
        sendPrivateMessage(uid, message_codeforces_all())
    # atcoder的比赛信息
    elif type == 'at':
        sendPrivateMessage(uid, message_atcoder_all())
    # 牛客的比赛信息
    elif type == 'nk':
        sendPrivateMessage(uid, message_newcoder_all())


def privateMessageJudgement(message, uid, nickname):
    """
    将私聊信息进行判断，如果触发了关键词，则进行相应操作
    :param message: 私聊的信息
    :param uid: 对方的 qq号
    :param nickname: 对方的 qq 昵称
    :return: null，打印这条信息并发送相应比赛信息
    """
    if message == "atcoder -c" or message == "at -c":
        # print(uid, nickname, message)
        sendPrivateContest('at', uid)
    if message == "nowcoder -c" or message == "nk -c":
        # print(uid, nickname, message)
        sendPrivateContest('nk', uid)
    if message == "cf -c" or message == "cf contests":
        # print(uid, nickname, message)
        sendPrivateContest('cf', uid)


def groupMessageJudgement(message, group_id, uid, nickname, qqnumber):
    """
    对群聊消息进行判断，如果触发了关键词，则进行相应操作
    :param message: 群聊信息中的信息
    :param group_id: qq群号
    :param uid: 用户的qq号 --暂时没用，主要用于拓展其他业务
    :param nickname: 用户的昵称
    :param qqnumber: 本机号码，用于@识别防误触的
    :return: null，打印这条消息，发送比赛信息
    """
    flag = True
    if "[CQ:at,qq=" + qqnumber + "]" not in message:
        return
    if "atcoder -c" in message or "at -c" in message:
        # print(uid, nickname, message)
        sendGroupContest('at', group_id)
        flag = False
    if "nowcoder -c" in message or "nk -c" in message:
        # print(uid, nickname, message)
        sendGroupContest('nk', group_id)
        flag = False
    if "cf -c" in message or "cf contests" in message:
        # print(uid, nickname, message)
        sendGroupContest('cf', group_id)
        flag = False
    if flag:
        if 'cf-' in message or 'cf -' in message:
            sendGroupContest('cf', group_id)
        if 'at-' in message or 'at -' in message:
            sendGroupContest('at', group_id)
        if 'nk-' in message or 'nk -' in message:
            sendGroupContest('nk', group_id)


def autosendmessage(group_id, testgroup_id):
    """
    1.查看是否已经又锁进行消息的发送
    2.通过调用各部分的函数进行消息的拼接
    3.有比赛向目标群发送消息否则发送到测试群告诉无消息
    :param group_id: 目标群群号
    :param testgroup_id: 测试群群号
    :return: null，直接给相应的群发送相应的消息
    """
    # 判断是否又文件锁
    if os.path.exists('./automessage.lock'):
        return
    f = open('automessage.lock', 'w')
    f.write("automessage")
    time.sleep(61)

    message = "今日比赛:\n"
    flag = 0
    error = 0

    # 调用 codeforces 的函数拼接今日的cf比赛信息
    message_temp = message_codeforces_daily()
    if "ERROR" in message_temp:
        error = 1
        message += "CF比赛无法获取\n" + message_temp
    else:
        if message_temp != "NULL":
            flag += 1
            message += "\n" + message_temp

    # 调用 atcoder 的函数拼接今日的at比赛信息
    message_temp = message_atcoder_daily()
    if message_temp != "NULL":
        flag += 1
        message += "\n" + message_temp

    # 调用 牛客 的函数拼接今日的牛客比赛信息
    message_temp = message_newcoder_daily()
    if message_temp != "NULL":
        flag += 1
        message += "\n" + message_temp

    # 判断是否有比赛，如有发送到目标群，如无发送到测试群
    if flag != 0:
        sendGroupMessage(group_id, message)
    else:
        if error:
            message = "CF比赛信息无法获取\n" + message_codeforces_all() + "\n"
            sendGroupMessage(testgroup_id, message)
        else:
            message = "今日无比赛，近日的CF比赛如下：\n\n"
            message += message_codeforces_all()
            sendGroupMessage(testgroup_id, message)

    # 释放文件锁
    f.close()
    os.remove('./automessage.lock')


def autoGetContest():
    if os.path.exists('./autoget.lock'):
        return
    f = open('autoget.lock', 'w')
    f.write("autoget")
    time.sleep(61)

    contestDBoperate.codeforce_daliy_DB()
    # contestDBoperate.atcodert_daliy_DB()
    contestDBoperate.newcoder_daliy_DB()

    f.close()
    os.remove('./autoget.lock')
