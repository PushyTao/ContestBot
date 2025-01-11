import httpx
from datetime import datetime
from httpx import HTTPError
from bs4 import BeautifulSoup


def get_nowcoder_contests():
    """
    爬取牛客网的比赛
    :return: 返回[{name:, link:, contest_time:}]
    """
    # nk_url是牛客系列赛, school_url是高校系列赛
    nk_url = 'https://ac.nowcoder.com/acm/contest/vip-index?topCategoryFilter=13'
    # school_url = 'https://ac.nowcoder.com/acm/contest/vip-index?topCategoryFilter=14'
    try:
        nk_get = httpx.get(url=nk_url, timeout=3)
        # school_get = httpx.get(url=school_url, timeout=3)
    except HTTPError as e:
        print(f'获取牛客比赛失败 http_code={e}')
        return
    data = BeautifulSoup(nk_get, 'html.parser'). \
        find_all('div', 'platform-item js-item')
    contest = []
    for i in data:
        h4 = i.h4
        name = h4.a.string
        link = 'https://ac.nowcoder.com' + h4.a['href']
        _ = [x.string.strip().replace('\n', '').replace('：', ' ').split()
             for x in i.ul.find_all('li')]
        _id = h4.a['href'].split('/')
        register_time = (
            datetime.strptime(' '.join(_[0][1:3:]), '%Y-%m-%d %H:%M'),
            datetime.strptime(' '.join(_[0][4:6:]), '%Y-%m-%d %H:%M')
        )
        if register_time[1] < datetime.now():
            continue
        contest_time = (
            datetime.strptime(' '.join(_[1][1:3:]), '%Y-%m-%d %H:%M'),
            datetime.strptime(' '.join(_[1][4:6:]), '%Y-%m-%d %H:%M')
        )
        contest.append({
            'id' : 'nk_'+str(_id[len(_id) - 1]),
            'name': name,
            'link': link,
            'contest_time': contest_time
        })

    return contest

def message_formate(contest):
    """
    一条比赛信息的拼接格式
    :param contest: 比赛的一个字典
    :return: 格式化好的 message
    """
    contest_time = list(map(str, contest['contest_time']))
    message = " 	比赛名称 : " + contest['name'] + "     \n" \
               + " 	比赛链接： " + contest['link'] + "     \t\n" \
               + " 	开始时间 : " + contest_time[0] + "     \t\n" \
               + " 	结束时间 : " + contest_time[1] + "     \t\n\n"
    return message

def message_newcoder_daily():
    """
    拼接 今日 牛客系列比赛 的比赛信息
    :return: 如果返回 拼接好的 message，如果没有 返回 NULL
    """
    todaydate = datetime.now().strftime('%Y-%m-%d')
    contests = get_nowcoder_contests()
    message = "牛客：\n"
    if len(contests) == 0:
        return "NULL"
    flag = False
    for x in contests:
        contest_time = list(map(str, x['contest_time']))
        timet = contest_time[0].split()
        if timet[0] != todaydate:
            continue
        flag = True
        message += message_formate(x)
    if flag:
        return message
    else:
        return "NULL"


def message_newcoder_all():
    """
    拼接所有的 牛客 的比赛信息
    :return: 拼接好的 message
    """
    contests = get_nowcoder_contests()
    message = "《牛客比赛日历》\n"
    if len(contests) == 0:
        message += "[空空如也]\t\t\n\n"
        return message
    for x in contests:
        message += message_formate(x)
    now_time = datetime.now()
    now_time = datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
    message = message + "更新时间 : " + now_time
    return message
