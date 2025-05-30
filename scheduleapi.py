import requests
import schedule
import time
import threading
import os

# 定义定时任务文件的路径
TIMER_TASKS_FILE = 'timer_tasks.txt'

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

