import httpx
from bs4 import BeautifulSoup
from httpx import HTTPError
from datetime import datetime, timedelta

import util


def get_atcoder_contests():
    """
    爬取atcoder的比赛
    :return: 返回[{name:, link:, contest_time:}]
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36 Edg/132.0.0.0'}
    global data
    try:
        data = httpx.get("https://atcoder.jp/contests", headers=headers, timeout=5)
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
        _id = k[1].a['href'].split('/')

        contest.append({
            'id': "at_" + _id[len(_id) - 1],
            'name': name,
            'link': link,
            'contest_time': (begin_time, end_time)
        })

    return contest


def message_atcoder_daily():
    """
    拼接 今日atcoder 的比赛信息
    :return: 如果返回 拼接好的 message，如果没有 返回 NULL
    """
    return util.message_codeforces_daily('at', 'Atcoder')


def message_atcoder_all():
    """
    拼接所有的atcoder的比赛信息
    :return: 拼接好的 message
    """
    return util.message_codeforces_all('at', 'Atcoder')
