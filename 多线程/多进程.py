import multiprocessing
from time import sleep, ctime

'''
# 直接生成Process实例
def clock(interval):
    while True:
        print('The time is %s' % ctime())
        sleep(interval)

if __name__ == '__main__':
    p = multiprocessing.Process(target=clock, args=(5,))
    p.start()
'''

"""
# 派生子类
class ClockProcess(multiprocessing.Process):
    '''
    两个函数比较重要
    1，init构造函数
    2，run函数，执行多进程的时候，实际就是执行run函数
    '''

    def __init__(self, interval):
        super().__init__()
        self.interval = interval

    def run(self):
        while True:
            print('The time is %s' % ctime())
            sleep(self.interval)

if __name__ == '__main__':
    p = ClockProcess(3)
    p.start()
    
"""

'''
from multiprocessing import Process
import os
def info(title):
    print(title)
    # __name__ 表示当前进程的名字
    print('module name: ', __name__)
    # 得到父亲进程的id
    print('parent process: ', os.getppid())
    # 得到本进程的id
    print('process id: ', os.getpid())

def f(name):
    info('funcion f')
    print('hello', name)

if __name__ == '__main__':
    info('main thread')
    # 创建子进程
    p = Process(target=f, args=('bob', ))
    p.start()
    p.join()
    
'''

import multiprocessing
from time import ctime

'''
def consumer(input_q):
    print('Into consumer: ', ctime())
    while True:
        # 处理锁
        item = input_q.get()
        print('pull', item, 'out of q') # 此处替换为有用的工作
        input_q.task_done() # 发出信号通知任务完成
    print('Out of consumer: ', ctime()) # 此句未执行，因为q.join()收集到四个task_done()信号后，主进程启动，未等到print这一句

def producer(sequence, output_q):
    print('Into producer: ', ctime())
    for item in sequence:
        output_q.put(item)
        print('put ', item, ' into q')
    print('Out of producer: ', ctime())

if __name__ == '__main__':
    q = multiprocessing.JoinableQueue()
    # 建立消费者进程
    cons_p = multiprocessing.Process(target=consumer(), args=(q, ))
    cons_p.daemon = True
    cons_p.start()

    # 生产多个项，sequence 代表要发送给消费者的项序列
    # 在实践中，这可能是生成器的输出或通过一些其它方式生产出来
    sequence = [1, 2, 3, 4]
    producer(sequence, q)
    
'''

# 设置哨兵
def consumer(input_q):
    print('Into consumer: ', ctime())
    while True:
        # 处理锁
        item = input_q.get()
        if item is None:
            break
        print('pull', item, 'out of q') # 此处替换为有用的工作
    print('Out of consumer: ', ctime()) # 此句未执行，因为q.join()收集到四个task_done()信号后，主进程启动，未等到print这一句

def producer(sequence, output_q):
    print('Into producer: ', ctime())
    for item in sequence:
        output_q.put(item)
        print('put ', item, ' into q')
    print('Out of producer: ', ctime())

if __name__ == '__main__':
    q = multiprocessing.Queue()
    # 建立消费者进程
    cons_p1 = multiprocessing.Process(target=consumer, args=(q, ))
    cons_p1.start()

    cons_p2 = multiprocessing.Process(target=consumer, args=(q, ))
    cons_p2.start()

    # 生产多个项，sequence 代表要发送给消费者的项序列
    # 在实践中，这可能是生成器的输出或通过一些其它方式生产出来
    sequence = [1, 2, 3, 4]
    producer(sequence, q)

    q.put(None)
    q.put(None)

    cons_p1.join()
    cons_p2.join()