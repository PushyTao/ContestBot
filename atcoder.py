import httpx
from bs4 import BeautifulSoup
from httpx import HTTPError
from datetime import datetime, timedelta


def get_atcoder_contests():
    """
    爬取atcoder的比赛
    :return: 返回[{name:, link:, contest_time:}]
    """
    global data
    try:
        data = httpx.get("https://atcoder.jp/contests", timeout=5)
    except HTTPError as e:
        print(f'获取atcoder比赛失败 http_code={e}')
        return []

    contest = []
    soup = BeautifulSoup(data, 'html.parser').body.div
    tr = soup.find(id="contest-table-upcoming").tbody.find_all('tr')

    for i in tr:
        k = i.find_all('td')
        # time
        t = k[0].time.string
        # 小鬼子比咱快一个小时，得减去
        begin_time = datetime.strptime(t, '%Y-%m-%d %H:%M:%S+0900') - timedelta(hours=1)
        # name
        name = k[1].a.string
        # link
        link = 'https://atcoder.jp' + k[1].a['href']
        # length
        hour, minute = map(int, k[2].string.split(':'))
        end_time = begin_time + timedelta(hours=hour, minutes=minute)

        contest.append({
            'name': name,
            'link': link,
            'contest_time': (begin_time, end_time)
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

def message_atcoder_daily():
    """
    拼接 今日atcoder 的比赛信息
    :return: 如果返回 拼接好的 message，如果没有 返回 NULL
    """
    contests = get_atcoder_contests()
    todaydate = datetime.now().strftime('%Y-%m-%d')

    message = "Atcoder:\n"
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


def message_atcoder_all():
    """
    拼接所有的atcoder的比赛信息
    :return: 拼接好的 message
    """
    contests = get_atcoder_contests()
    message = "《Atcoder比赛日历》\n"
    if len(contests) == 0:
        message += "[空空如也]\t\t\n\n"
        return message
    for x in contests:
        message += message_formate(x)
    now_time = datetime.now()
    now_time = datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
    message = message + "更新时间 : " + now_time
    return message
