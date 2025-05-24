from flask import Flask
from flask import request
import api

app=Flask(__name__)

@app.route('/',methods=["post"])
def post_data():
    if request.get_json().get('message_type')=='private':
        uid=request.get_json().get('sender').get('user_id')
        message=request.get_json().get('raw_message')
        api.keyword(message,uid)
    if request.get_json().get('message_type')=='group':
        gid=request.get_json().get('group_id')
        uid=request.get_json().get('sender').get('user_id') 
        message=request.get_json().get('raw_message') 
        api.keyword(message, uid, gid)

    return 'OK'

if __name__ == '__main__':
    # 启动定时任务
    api.start_scheduler()
    print("定时任务系统已启动")
    app.run(debug=False, host='127.0.0.1', port=8000)  # 关闭调试模式