import DB
import atcoder
import codeforces
import methods
import newcoder


def contest_update(id, name, starttime, endtime, platform, link):
    """
    如果比赛已经存在就对其信息进行修改，确保信息最新
    如果比赛不存在就将比赛插入到数据库中
    :param id: 比赛的id
    :param name: 比赛的名称
    :param starttime: 比赛开始时间
    :param endtime: 比赛结束时间
    :param platform: 比赛平台
    :param link: 比赛链接
    :return: null
    """
    selectContestSql = "select * from contest where id='" + id + "'"
    selectData = DB.sqlselect(selectContestSql)
    print(selectData)
    if selectData == 'select error':
        print("数据库查询有错误，请检查代码语句")
        methods.sendGroupMessage('949525561', '数据库select有问题，速查')
        return
    if len(selectData) == 0:
        insertContestSql = "insert into contest(id,platform,contestname,starttime,endtime,link,count,teamcontest,deleted)" + \
                           "values('" + id + "','" + platform + "','" + name + \
                           "','" + starttime + "','" + endtime + \
                           "','" + link + "','-1','0','0')"
        DB.sqloperate(insertContestSql)
    else:
        updateContestSql = "update contest set contestname='" + name + "'," + \
                           "starttime='" + starttime + "'," + \
                           "endtime='" + endtime + "'" + " where id='" + id + "'"
        print(updateContestSql)
        DB.sqloperate(updateContestSql)


def codeforce_daliy_DB():
    """
    从at网站获取比赛日历，对每个比赛进行查询
    如果比赛已经存在就对其信息进行修改，确保信息最新
    如果比赛不存在就将比赛插入到数据库中
    :return: null
    """
    codeforcescontest = codeforces.get_codeforces_contests()
    for contest in codeforcescontest:
        contest_update(contest['id'], contest['name'], contest['begin_time'], contest['end_time'], 'cf',
                       contest['link'])


def atcodert_daliy_DB():
    """
    从cf网站获取比赛日历，对每个比赛进行查询
    如果比赛已经存在就对其信息进行修改，确保信息最新
    如果比赛不存在就将比赛插入到数据库中
    :return: null
    """
    atcodercontest = atcoder.get_atcoder_contests()
    for contest in atcodercontest:
        contest_time = list(map(str, contest['contest_time']))
        contest_update(contest['id'], contest['name'], contest_time[0], contest_time[1], 'at', contest['link'])


def newcoder_daliy_DB():
    """
    从 牛客 网站获取比赛日历，对每个比赛进行查询
    如果比赛已经存在就对其信息进行修改，确保信息最新
    如果比赛不存在就将比赛插入到数据库中
    :return: null
    """
    newcodercontest = newcoder.get_nowcoder_contests()
    for contest in newcodercontest:
        contest_time = list(map(str, contest['contest_time']))
        contest_update(contest['id'], contest['name'], contest_time[0], contest_time[1], 'nk', contest['link'])


def select_contest(platform):
    selectcontestsql = "select * from contest where platform='" + platform + "' order by starttime asc"
    selectData = DB.sqlselect(selectcontestsql)
    contestData = []
    for contest in selectData:
        if contest[8] == 0 and contest[7] == 0:
            contestData.append({
                'name': contest[2],
                'starttime': contest[3],
                'endtime': contest[4],
                'link': contest[5]
            })
    return contestData
