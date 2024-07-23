# import datetime
from datetime import datetime
import time

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry

import DB

url_cf = "http://codeforces.com/api"
RES = requests.session()
RES.mount('http://', HTTPAdapter(max_retries=Retry(total=5)))
RES.mount('https://', HTTPAdapter(max_retries=Retry(total=5)))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
}


def cfdeldiv1(contests):
    """
    将比赛中的 div 1 进行删除
    :param contests: 比赛所有信息的数组
    :return: 删除后 的比赛所有信息的数组
    """
    contest = []
    for i in contests:
        contestname = i["name"]
        if '(Div. 1)' in contestname:
            continue
        else:
            contest.append(i)
    return contest


def get_codeforces_contests():
    """
    爬取cf的比赛信息
    :return: 比赛信息的数组{name：比赛名字，begin_time:开始时间，end_time:结束时间，
    type:比赛类型，status:比赛状态，relative_time: ，id:比赛的id用于拼接比赛地址}
    """
    response = RES.get(url=url_cf + "/contest.list")
    while response.status_code != 200:
        response = RES.get(url=url_cf + "/contest.list")
        time.sleep(0.3)
    res = response.json().get("result")
    contests = []
    for i in res:
        if i.get("phase") == "FINISHED":
            break
        contest = {
            "name": i.get("name"),
            "begin_time": datetime.fromtimestamp(i.get("startTimeSeconds")).strftime('%Y-%m-%d %H:%M:%S'),
            "end_time": datetime.fromtimestamp(i.get("startTimeSeconds") + i.get("durationSeconds")).strftime(
                '%Y-%m-%d %H:%M:%S'),
            "type": i.get("type"),
            "status": i.get("phase"),
            "relative_time": i.get("relativeTimeSeconds"),
            "id": i.get("id"),
        }
        reset = abs(i.get("relativeTimeSeconds"))
        if reset > 7 * 24 * 60 * 60:
            continue
        contests.append(contest)
    return contests


def message_formate(contest):
    """
    一条比赛信息的拼接格式
    :param contest: 比赛的一个字典
    :return: 格式化好的 message
    """
    message = " 	比赛名称 : " + contest["name"] + "     \n" \
              + " 	比赛链接 : https://codeforces.com/contestRegistration/" + str(contest["id"]) + "     \t\n" \
              + " 	开始时间 : " + contest["begin_time"] + "     \t\n" \
              + " 	结束时间 : " + contest["end_time"] + "     \t\n" \
              + " 	比赛类型 : " + contest["type"] + "     \t\n"
    return message


def message_codeforces_daily():
    """
    拼接 今日codeforces 的比赛信息
    :return: 如果返回 拼接好的 message，如果没有 返回 NULL
    """
    todaydate = datetime.now().strftime('%Y-%m-%d')
    message = "codeforces:\n"
    contests = get_codeforces_contests()
    # contests = cfdeldiv1(contests)
    if len(contests) == 0:
        return "NULL"
    flag = False
    for i in contests[::-1]:
        timet = i['begin_time'].split()
        if timet[0] != todaydate:
            continue
        if i["status"] != "BEFORE":
            continue
        flag = True
        message += message_formate(i) + "\n"
    if flag:
        return message
    else:
        return "NULL"


def message_codeforces_all():
    """
    拼接所有的 codeforces 的比赛信息
    :return: 拼接好的 message
    """
    contests = get_codeforces_contests()
    message = "《Codeforces 比赛日历》\n "
    if len(contests) == 0:
        message += "[空空如也]\t\t\n\n"
        return message
    for i in contests[::-1]:
        message += message_formate(i)
        message += "\n"
        # if i["status"] != "BEFORE":
        #     message += " 	比赛状态 : 进行中...\t\n\n"
        # else:
        #     message += " 	比赛状态 : 未开始，距开始剩余 " + datetime.strftime(abs(i["relative_time"]), '%H:%M:%S') + "\t\n\n"
    now_time = datetime.now()
    now_time = datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
    message = message + "更新时间 : " + now_time
    return message


def getRating(use_id):
    """
    获取用户的信息包括当前分数，最大的分数，最后登录时间等信息
    :param use_id: ((学号，cf_id),(学号，cf_id))
    :return: {cf_id:[rating,maxrating,last_log_time],...}
    """
    url_userinfo = url_cf + '/user.info?handles=';
    for i in use_id:
        url_userinfo += i[1] + ';'

    response = RES.get(url=url_userinfo)
    while response.status_code != 200:
        response = RES.get(url=url_userinfo)
        time.sleep(0.3)
    res = response.json().get("result")
    info = {}
    for i in res:
        user = i.get("handle")
        maxrating = i.get("maxRating")
        rating = i.get("rating")
        last_log_time = datetime.fromtimestamp(i.get("lastOnlineTimeSeconds")).strftime('%Y-%m-%d %H:%M:%S')
        # last_log_time = time.strftime('%Y-%m-%d %H:%M:%S', i.get("lastOnlineTimeSeconds"))
        info.update({user: [rating, maxrating, last_log_time]});
    return info
