from datetime import datetime

import contestDBoperate

date_format = "%Y-%m-%d %H:%M:%S"

def is_today(date_time_str):
    # 解析字符串为datetime对象
    given_datetime = datetime.strptime(date_time_str, date_format)
    # 获取当前日期
    today = datetime.today()
    # 比较日期部分
    return given_datetime.date() == today.date()

def is_aftertime(date_time_str):
    current_date = datetime.now()
    input_date = datetime.strptime(date_time_str, date_format)
    if input_date >= current_date:
        return True
    return False

def message_formate(contest):
    """
    一条比赛信息的拼接格式
    :param contest: 比赛的一个字典
    :return: 格式化好的 message
    """
    message = " 	比赛名称 : " + contest["name"] + "\n" \
              + " 	比赛链接 : " + contest['link'] + "\n" \
              + " 	开始时间 : " + contest["starttime"] + "\n" \
              + " 	结束时间 : " + contest["endtime"] + "\n"
    return message

def message_codeforces_daily(type,message):
    """
    拼接 今日codeforces 的比赛信息
    :return: 如果返回 拼接好的 message，如果没有 返回 NULL
    """
    contestData = contestDBoperate.select_contest(type)
    message += ":\n"
    if len(contestData) == 0:
        return "NULL"
    flag = False
    for i in contestData:
        # 比赛日期不是今天
        if not is_today(i['starttime']):
            continue
        # 比赛已经结束
        if not is_aftertime(i['endtime']):
            continue
        flag = True
        message += message_formate(i) + "\n"
    if flag:
        return message
    else:
        return "NULL"

def message_codeforces_all(type,message1):
    """
    拼接所有的 codeforces 的比赛信息
    :return: 拼接好的 message
    """
    _contests = contestDBoperate.select_contest(type)
    contests = []
    for i in _contests:
        if not is_aftertime(i['starttime']):
            continue
        contests.append(i)
    message = "《" + message1 + " 比赛日历》\n "
    if len(contests) == 0:
        message += "[空空如也]\t\t\n\n"
        return message
    for i in contests:
        message += message_formate(i)
        message += "\n"
    now_time = datetime.now()
    now_time = datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
    message = message + "更新时间 : " + now_time
    return message