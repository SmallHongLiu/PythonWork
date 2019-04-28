import requests
from lxml import etree
import json
from dingtalkchatbot.chatbot import DingtalkChatbot

def get_new_part():
    base_url = r'https://www.dy2018.com/i/100723.html'
    res = requests.get(base_url)
    res.encoding = 'gbk'
    s = etree.HTML(res.text)
    part_num = s.xpath('//*[@id="Zoom"]/div/ul/li/a/text()')[0]
    return part_num, base_url

# 信息发送
url = webhook
header = {
    'Content-type': 'application/json',
    'charset': 'utf-8'
}

data = {
    'msgtype': 'text',
    'text': {'content': 'message'}
}

sendData = json.dumps(data)
requests = requests.post(url, data=sendData, headers=header)

webhook = '你的webhook码'
xiaoding = DingtalkChatbot(webhook)
xiaoding.send_text(msg='我就是小丁，小丁就是我!', is_at_all=True)


def get_old_part():
    with open('part_num.txt') as f:
        old_num = f.read()
    return old_num

def main():
    new_part, href = get_new_part()
    old_part = get_old_part()
    if old_part != new_part:
        send_msg(new_part)
        with open('part_num.txt', 'w') as f:
            f.write(new_part)

def send_msg(num):
    webhook = '你的webhook码'
    dd = DingtalkChatbot(webhook)
    dd.send_text(title='权利的游戏', text='#### 《权利的游戏》第八集\n'
                 '更新至' + num + '\n\n'
                 '![剧照](https://img.18qweasd.com/d/file/p/2019-04-15/\
                 0d084383f8b0b6d3a06561b4c4bbb337.jpg)\n'
                 '[观看地址](https://www.dy2018.com/i/100723.html) \n',
                 is_at_all=False)
