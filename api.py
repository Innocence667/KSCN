import json
import random
import re
import requests
import datetime
import time
import wget
import threading
import os
import base64
from flask import request

import scheduleapi

setu_cooldown = {}  #格式: {用户ID: 最后调用时间}

def keyword(message, uid, gid = None):
    if message[:]=='>help':
        usage(gid)
    if message[:]=='>来点涩图' or message[:]=='>setu':
        setu(gid,uid)
    # if message[:]=='>hello':
    #    hhw(gid)
    # if message[0:3]=='>ng':
    #     songid=message[4:]
    #     ngdownload(gid,songid)
    if message[:]=='>antigen test':
        adt(gid,uid)
    if message[0:4]=='>cat':
        if message[:]=='>cat':
            httpcat(gid,-1)
        else:
            picid=message[5:]
            httpcat(gid,picid)    # 处理定时消息命令
    if message.startswith('>timer') or message.startswith('>定时'):
        try:
            if message.startswith('>timer'):
                parts = message[6:].strip().split(' ', 2)  # 分割成时间和消息内容
            else:
                parts = message[3:].strip().split(' ', 2)  # 分割成时间和消息内容
                
            if len(parts) >= 2:
                time_str = parts[0]  # 时间格式 HH:MM
                msg_content = parts[1]
                scheduleapi.schedule_daily_message(gid, msg_content, time_str)
                requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message=已设置在每天 {1} 发送消息：{2}'.format(gid, time_str, msg_content))
            else:
                requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message=格式错误，正确格式为：>定时 HH:MM 消息内容'.format(gid))
        except Exception as e:
            requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message=设置定时消息失败：{1}'.format(gid, str(e)))

# 启动定时任务线程
def start_scheduler():
    # 从文件加载任务
    tasks = scheduleapi.load_tasks_from_file()
    for time_str, group_id, message in tasks:
        try:
            scheduleapi.schedule_daily_message(group_id, message, time_str, save_to_file=False)
            # print(f"已加载定时任务: {time_str} 发送到群 {group_id}")
        except Exception as e:
            print(f"加载定时任务失败: {time_str} {group_id} - {str(e)}")
    
    # 启动定时器线程
    scheduler_thread = threading.Thread(target=scheduleapi.run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    print(f"定时任务系统已启动，已加载 {len(tasks)} 个任务")

def adt(gid,uid):
    requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message=测试中...'.format(gid))
    num=random.randint(1,100)
    time.sleep(3)
    if num<=82:
        requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}- C{2}  T{3}  S{4} 是阴性呢'.format(gid,r'[CQ:at,'r'qq='+str(uid)+r']'+'\n','\n','\n','\n'))
    elif num<=86:
        requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}  C{2}  T{3}  S{4} 无效的测试结果，可能是加少了'.format(gid,r'[CQ:at,'r'qq='+str(uid)+r']'+'\n','\n','\n','\n'))
    elif num<=90:
        requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}  C{2}- T{3}  S{4} 无效的测试结果，可能是加多了'.format(gid,r'[CQ:at,'r'qq='+str(uid)+r']'+'\n','\n','\n','\n'))
    else:
        requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}- C{2}- T{3}  S{4} 诶呀，你阳了'.format(gid,r'[CQ:at,'r'qq='+str(uid)+r']'+'\n','\n','\n','\n'))
def usage(gid):
    requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message=使用说明请点击:https://docs.qq.com/doc/DYkZnRHhKVE9WTFZK'.format(gid))

def ngdownload(gid,songid):
    requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message=正在下载中...'.format(gid))
    url='https://www.newgrounds.com/audio/download/'+songid
    name=songid+'.mp3'
    path='C:/BotFiles/Songs/'+songid+'.mp3'
    print(url)
    wget.download(url,path)
    requests.get(url='http://127.0.0.1:5700/upload_group_file?group_id={0}&file={1}&name={2}'.format(gid,path,name))

def setu(gid,uid):
    if gid==594936663: return
    # 如果提供了用户 ID，检查该用户是否在冷却时间内
    if uid is not None:
        current_time = time.time()
        last_call_time = setu_cooldown.get(uid, 0)
        # 检查是否在一分钟冷却时间内
        if current_time - last_call_time < 60:
            remaining = int(60 - (current_time - last_call_time))
            requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message=不许涩涩！你需要再等{1}秒才能用这个功能！'.format(gid, remaining))
            return
        # 更新用户最后调用时间
        setu_cooldown[uid] = current_time
    
    url='https://api.lolicon.app/setu/v2?size=original&size=regular'
    menu=requests.get(url)
    setu_url=menu.json()['data'][0]['urls']['regular']
    # print(setu_url)
    msg_menu=requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid,r'[CQ:image,'r'file='+str(setu_url)+r']'))
    msg_id=msg_menu.json()['data']['message_id']
    # print(msg_id)
    time.sleep(60)
    requests.get(url='http://127.0.0.1:5700/delete_msg?message_id={0}'.format(msg_id))

def hhw(gid):
    requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message=Hello, world!'.format(gid))

def httpcat(gid,picid):
    if(picid==-1):
        arr=[100,101,102,103,200,201,202,203,204,206,207,300,301,302,303,304,305,307,308,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,421,422,423,424,425,426,429,431,444,450,451,497,498,499,500,501,502,503,504,506,507,508,509,510,511,521,522,523,525,599]
        num=random.randint(0,65)
        url='https://http.cat/'+str(arr[num])
        requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid,r'[CQ:image,'r'file='+str(url)+r']'))
    else:
        url='https://http.cat/'+str(picid)
        requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid,r'[CQ:image,'r'file='+str(url)+r']'))

def poke(gid, uid):
    with open('kscnconfig.json','r') as f:
        config = json.load(f)
    num=random.randint(0,14)
    image_path= os.path.join(config['poke_image_folder'], f"{num}.jpg") # 使用配置文件中的图片路径
    file_url=f"file://{image_path}"
    requests.get(url='http://127.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(
        gid, f'[CQ:image,file={file_url}]'))