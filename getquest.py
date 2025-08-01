from flask import Flask
from flask import request

import api

app=Flask(__name__)

@app.route('/',methods=["post"])
def post_data():
    data = request.get_json()
    
    # 处理消息事件
    if data.get('post_type') == 'message':
        if data.get('message_type') == 'private':
            uid = data.get('sender').get('user_id')
            message = data.get('raw_message')
            api.keyword(message, uid)
        elif data.get('message_type') == 'group':
            print(data)
            gid = data.get('group_id')
            uid = data.get('sender').get('user_id') 
            message = data.get('raw_message')
            api.keyword(message, uid, gid)
    
    # 处理通知事件
    elif data.get('post_type') == 'notice':
        notice_type = data.get('notice_type')
        
        # 处理戳一戳事件
        if notice_type == 'notify' and data.get('sub_type') == 'poke':
            gid=data.get('group_id')
            uid=data.get('user_id')  # 戳人的人
            target_id=data.get('target_id')  # 被戳的人
            bot_qq=2079261252
            if target_id == bot_qq:
                # print(f"机器人被{uid}戳了一下，在群{gid}")
                api.poke(gid, uid)

    return 'OK'

if __name__ == '__main__':
    # 启动定时任务
    api.start_scheduler()
    print("定时任务系统已启动")
    app.run(debug=False, host='127.0.0.1', port=8000)  # 关闭调试模式