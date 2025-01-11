from flask import Flask, request

import settingConfig
from methods import *

app = Flask(__name__)


@app.route('/', methods=["POST"])
def post_data():
    """
    主程序，根据时间自动发送消息，根据监听到的消息进行相关操作
    :return:
    """
    timenow = time.strftime("%H:%M", time.localtime())
    if timenow == settingConfig.settingNumber()['autoSendTime']:  # 定时发送的时间
        numbers = settingConfig.settingNumber()
        autonumber = numbers['sendGroupNumber']
        autotestnumber = numbers['monitorGroupNumber']
        autosendmessage(autonumber, autotestnumber)

    if timenow == settingConfig.settingNumber()['autoGetTime']:
        autoGetContest();

    if request.get_json().get("message_type") == "private":  # 如果是私聊信息
        uid = request.get_json().get('sender').get('user_id')  # 获取信息发送者的 QQ号码
        nickname = request.get_json().get("sender").get("nickname")
        message = request.get_json().get('raw_message')  # 获取原始信息
        privateMessageJudgement(message, uid, nickname)

    if request.get_json().get('message_type') == 'group':  # 如果是群聊信息
        gid = request.get_json().get('group_id')  # 获取群号
        uid = request.get_json().get('sender').get('user_id')  # 获取信息发送者的 QQ号码
        nickname = request.get_json().get("sender").get("nickname")
        message = request.get_json().get('raw_message')  # 获取原始信息
        print(uid, nickname, message)
        qqnumber = settingConfig.settingNumber()['user']
        groupMessageJudgement(message, gid, uid, nickname, qqnumber)
    return "OK"


if __name__ == '__main__':
    # 先将文件锁删除，确保之前没有锁
    if os.path.exists('./automessage.lock'):
        os.remove('./automessage.lock')
    if os.path.exists('./autoget.lock'):
        os.remove('./autoget.lock')
    post = settingConfig.settingPost()
    host_data = post['host']
    port_data = post['port']
    app.run(debug=True, host=host_data, port=port_data)
