import requests
from bs4 import BeautifulSoup
import os
from urllib import request
import threading

BASE_URL = 'https://www.doutula.com/photo/list/?page='
# 页面的url列表
PAGE_URL_LIST = []
# 所有表情的url列表
FACE_URL_LIST = []
# 全局锁
gLock = threading.Lock()

for i in range(1, 870):
    url = BASE_URL + str(i)
    PAGE_URL_LIST.append(url)


# 下载图片
def download_image(url):
    my_headers = [('User - Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.17'
                                   ' (KHTML, like Gecko) Version/3.1 Safari/525.17')]
    opener = request.build_opener()
    opener.addheaders = my_headers
    request.install_opener(opener)

    split_list = url.split('/')
    filename = split_list.pop()
    path = os.path.join('images', filename)
    request.urlretrieve(url, filename=path)


def get_page(page_url):
    pass


def producer():
    while True:
        gLock.acquire()
        if len(PAGE_URL_LIST) == 0:
            gLock.release()
            break
        else:
            page_url = PAGE_URL_LIST.pop()
            gLock.release()
            response = requests.get(page_url)
            content = response.content
            soup = BeautifulSoup(content, 'lxml')
            img_list = soup.find_all('img', attrs={'class': 'img-responsive lazy image_dta loaded'})
            gLock.acquire()
            for img in img_list:
                face_url = img['data_original']
                if not face_url.startswith('https'):
                    face_url = 'https' + face_url
                FACE_URL_LIST.append(face_url)
            gLock.release()


def customer():
    while True:
        gLock.acquire()
        if len(FACE_URL_LIST) == 0:
            gLock.release()
            continue
        else:
            face_url = FACE_URL_LIST.pop()
            gLock.release()
            download_image(face_url)


def main():
    # 创建两个多线程来作为生产者，去爬取表情的url
    for i in range(3):
        th = threading.Thread(target=producer)
        th.start()

    # 创建4个线程来作为消费者，去下载表情图片
    for i in range(5):
        th = threading.Thread(target=customer)
        th.start()


if __name__ == '__main__':
    main()