import json
import random
import re
import requests
import datetime
import time
import schedule
import wget
import threading
import os
from flask import request

# 定义定时任务文件的路径
TIMER_TASKS_FILE = 'timer_tasks.txt'

def keyword(message, uid, gid = None):
    if message[:]=='>help':
        usage(gid)
    if message[:]=='>来点涩图' or message[:]=='>setu':
        setu(gid)
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
                schedule_daily_message(gid, msg_content, time_str)
                requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message=已设置在每天 {1} 发送消息：{2}'.format(gid, time_str, msg_content))
            else:
                requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message=格式错误，正确格式为：>定时 HH:MM 消息内容'.format(gid))
        except Exception as e:
            requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message=设置定时消息失败：{1}'.format(gid, str(e)))

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

def setu(gid):
    if gid==594936663: return
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

# 定时任务相关函数
def schedule_message(group_id, message, time_str):
    """
    设置定时发送消息任务
    
    参数:
    group_id (int): 群号
    message (str): 要发送的消息内容
    time_str (str): 时间字符串，格式为 "HH:MM" 如 "08:30"
    """
    schedule.every().day.at(time_str).do(send_scheduled_message, group_id=group_id, message=message)
    # 保存到文件中
    save_task_to_file(time_str, group_id, message)
    
def send_scheduled_message(group_id, message):
    """发送计划好的消息"""
    requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(group_id, message))
    return schedule.CancelJob  # 如果只想发送一次，返回CancelJob，否则删除此行

def schedule_daily_message(group_id, message, time_str, save_to_file=True):
    """设置每日定时消息"""
    schedule.every().day.at(time_str).do(send_scheduled_message, group_id=group_id, message=message)
    # 保存到文件中，但只有在需要时才保存
    if save_to_file:
        save_task_to_file(time_str, group_id, message)

def is_task_exists(time_str, group_id, message):
    """检查任务是否已存在于文件中"""
    if not os.path.exists(TIMER_TASKS_FILE):
        return False
        
    try:
        with open(TIMER_TASKS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split(' ', 2)
                if len(parts) >= 3:
                    if parts[0] == time_str and int(parts[1]) == group_id and parts[2] == message:
                        return True
        return False
    except Exception:
        return False  # 出错时假设任务不存在

def save_task_to_file(time_str, group_id, message):
    """将定时任务保存到文件，避免重复添加相同的任务"""
    # 检查任务是否已存在
    if is_task_exists(time_str, group_id, message):
        return True  # 如果任务已存在，无需再次添加
        
    try:
        with open(TIMER_TASKS_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{time_str} {group_id} {message}\n")
        return True
    except Exception as e:
        print(f"保存定时任务到文件时出错：{str(e)}")
        return False

def load_tasks_from_file():
    if not os.path.exists(TIMER_TASKS_FILE):
        return []
    
    tasks = []
    try:
        with open(TIMER_TASKS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                parts = line.split(' ', 2)
                if len(parts) >= 3:
                    time_str = parts[0]
                    group_id = int(parts[1])
                    message = parts[2]
                    tasks.append((time_str, group_id, message))
        return tasks
    except Exception as e:
        print(f"从文件加载定时任务时出错：{str(e)}")
        return []

def run_scheduler():
    """运行定时任务"""
    while True:
        schedule.run_pending()
        time.sleep(1)

# 启动定时任务线程
def start_scheduler():
    # 从文件加载任务
    tasks = load_tasks_from_file()
    for time_str, group_id, message in tasks:
        try:
            schedule_daily_message(group_id, message, time_str, save_to_file=False)
            # print(f"已加载定时任务: {time_str} 发送到群 {group_id}")
        except Exception as e:
            print(f"加载定时任务失败: {time_str} {group_id} - {str(e)}")
    
    # 启动定时器线程
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    print(f"定时任务系统已启动，已加载 {len(tasks)} 个任务")

