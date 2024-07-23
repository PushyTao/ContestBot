import pymysql

import settingConfig


def connectDB():
    DBINFO = settingConfig.settingDb()
    hostInfo = DBINFO['host']
    userInfo = DBINFO['user']
    passwdInfo = DBINFO['passwd']
    postInfo = int(DBINFO['port'])
    dbInfo = DBINFO['db']
    charsetInfo = DBINFO['charset']
    # 连接数据库
    conn = pymysql.connect(host=hostInfo  # 连接名称，默认127.0.0.1
                           , user=userInfo  # 用户名
                           , passwd=passwdInfo  # 密码
                           , port=postInfo  # 端口，默认为3306
                           , db=dbInfo  # 数据库名称
                           , charset=charsetInfo  # 字符编码
                           )
    return conn


def sqlselect(sql):
    conn = connectDB()
    cur = conn.cursor()  # 生成游标对象
    # sql = "select * from student_info"  # SQL语句
    try:
        cur.execute(sql)  # 执行SQL语句
        data = cur.fetchall()  # 通过fetchall方法获得数据
    except:
        conn.rollback()
        data = "select error"
    cur.close()  # 关闭游标
    conn.close()  # 关闭连接
    return data


def sqloperate(sql):
    conn = connectDB()
    cur = conn.cursor()  # 生成游标对象
    try:
        cur.execute(sql)  # 执行SQL语句
        conn.commit()
    except:
        conn.rollback()  # 如果发生错误则回滚
    cur.close()  # 关闭游标
    conn.close()  # 关闭连接
    return "OK"
