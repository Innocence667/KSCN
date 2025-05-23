import json
import random
import re
import requests
import datetime
import time
import schedule
import wget
from flask import request

def keyword(message, uid, gid = None):
    if message[:]=='>help' or message[:]=='>使用帮助':
        usage(gid)
    if message[:]=='>来点涩图' or message[:]=='>setu':
        setu(gid)
    if message[0:5]=='>hello':
        hhw(gid)
    if message[0:3]=='>ng':
        songid=message[4:]
        ngdownload(gid,songid)
    if message[:]=='>antigen test':
        adt(gid)
    if message[0:4]=='>cat':
        if message[:]=='>cat':
            httpcat(gid,-1)
        else:
            picid=message[5:]
            httpcat(gid,picid)

def adt(gid):
    requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message=测试中...'.format(gid))
    num=random.randint(1,100)
    time.sleep(5)
    if num<=82:
        requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message=- C{1}  T{2}  S'.format(gid,'\n','\n'))
        requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message=是阴性呢'.format(gid))
    elif num<=86:
        requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message=  C{1}  T{2}  S'.format(gid,'\n','\n'))
        requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message=无效的测试结果，可能是加少了'.format(gid))
    elif num<=90:
        requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message=  C{1}- T{2}  S'.format(gid,'\n','\n'))
        requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message=无效的测试结果，可能是加多了'.format(gid))
    else:
        requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message=- C{1}- T{2}  S'.format(gid,'\n','\n'))
        requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message=诶呀，你阳了'.format(gid))
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
    print(setu_url)
    msg_menu=requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid,r'[CQ:image,'r'file='+str(setu_url)+r']'))
    msg_id=msg_menu.json()['data']['message_id']
    print(msg_id)
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

