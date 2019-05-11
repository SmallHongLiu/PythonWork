'''多线程'''

import threading
import time


def greet(index):
    print('hello world - %d' % index)
    time.sleep(1)


# 同步执行
def line_run():
    for x in range(5):
        greet(x)


# 异步执行
def async_run():
    for x in range(5):
        th = threading.Thread(target=greet, args=[x])
        th.start()


if __name__ == '__main__':
    async_run()


'''生产者-消费者'''
import random

gLock = threading.Lock()


def Producer():
    while True:
        global MONEY
        random_money = random.randint(10, 100)
        gLock.acquire()  # 获取锁
        MONEY += random_money
        gLock.release()  # 释放锁
        print('生产者: %s生成了%d' % (threading.current_thread(), random_money))
        time.sleep(0.5)


def Customer():
    while True:
        global MOENY
        random_money = random.randint(10, 100)
        if MOENY > random_money:
            print('消费了：%s消费了%d' % (threading.current_thread(), random_money))
            gLock.acquire()
            MOENY -= random_money
            gLock.release()
        else:
            print('需要消费的钱为：%d, 余额为：%d' % (random_money, MOENY))
        time.sleep(0.5)


def p_c_test():
    # 执行3个线程，来当作生产者
    for i in range(3):
        th = threading.Thread(target=Producer)
        th.start()

    # 执行3个线程，来当作消费者
    for i in range(3):
        th = threading.Thread(target=Customer)
        th.start()