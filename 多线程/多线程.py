'''
利用time函数，生成两个函数
顺序调用
计算总的运行时间
'''

'''
import time
def loop1():
    # ctime 得到当前时间
    print('Start loop 1 at: ', time.ctime())
    time.sleep(4)
    print('End loop 1 at: ', time.ctime())

def loop2():
    print('Start loop 2 at: ', time.ctime())
    time.sleep(2)
    print('End loop 2 at: ', time.ctime())

def main():
    print('Starting at: ', time.ctime())
    loop1()
    loop2()
    print('All done at: ', time.ctime())

if __name__ == '__main__':
    main() 
'''

'''
import time
import _thread as thread

def loop1():
    # ctime 得到当前时间
    print('Start loop 1 at: ', time.ctime())
    time.sleep(4)
    print('End loop 1 at: ', time.ctime())

def loop2():
    print('Start loop 2 at: ', time.ctime())
    time.sleep(2)
    print('End loop 2 at: ', time.ctime())

def main():
    print('Starting at: ', time.ctime())
    # 启动多线程的意思就是用多线程去执行某个函数
    # 启动多线程的函数为start_new_thread
    # 参数两个，第一个：需要运行的函数的名字，第二个：函数的参数作为元祖使用，如果函数没有参数，则使用空元祖，如下所示
    thread.start_new_thread(loop1, ())
    thread.start_new_thread(loop2, ())
    print('All done at: ', time.ctime())

if __name__ == '__main__':
    main()
'''

'''
# 多线程传参数
import time
import _thread as thread

def loop1(in1):
    # ctime 得到当前时间
    print('Start loop 1 at: ', time.ctime())
    print('我是参数：', in1)
    time.sleep(4)
    print('End loop 1 at: ', time.ctime())

def loop2(in1, in2):
    print('Start loop 2 at: ', time.ctime())
    print('我是参数: ', in1, '和参数: ', in2)
    time.sleep(2)
    print('End loop 2 at: ', time.ctime())

def main():
    print('Starting at: ', time.ctime())
    # 启动多线程的意思就是用多线程去执行某个函数
    # 启动多线程的函数为start_new_thread
    # 参数两个，第一个：需要运行的函数的名字，第二个：函数的参数作为元祖使用，如果函数没有参数，则使用空元祖，如下所示
    thread.start_new_thread(loop1, ("SmallHong", )) # 注意：当只有一个参数数，后面须加一个逗号，因为这个地方参数是一个元祖类型
    thread.start_new_thread(loop2, ('SmallHong', 'BigHui'))
    print('All done at: ', time.ctime())
'''

'''
# threading 案例
import time
import threading

def loop1(in1):
    # ctime 得到当前时间
    print('Start loop 1 at: ', time.ctime())
    print('我是参数：', in1)
    time.sleep(4)
    print('End loop 1 at: ', time.ctime())

def loop2(in1, in2):
    print('Start loop 2 at: ', time.ctime())
    print('我是参数: ', in1, '和参数: ', in2)
    time.sleep(2)
    print('End loop 2 at: ', time.ctime())

def main():
    print('Starting at: ', time.ctime())
    t1 = threading.Thread(target=loop1, args=('SmallHong', ))
    t1.start()

    t2 = threading.Thread(target=loop2, args=('SmallHong', 'BigHui'))
    t2.start()
    print('All done at: ', time.ctime())

if __name__ == '__main__':
    main()
'''

'''
# threading加入join
import time
import threading

def loop1(in1):
    # ctime 得到当前时间
    print('Start loop 1 at: ', time.ctime())
    print('我是参数：', in1)
    time.sleep(4)
    print('End loop 1 at: ', time.ctime())

def loop2(in1, in2):
    print('Start loop 2 at: ', time.ctime())
    print('我是参数: ', in1, '和参数: ', in2)
    time.sleep(2)
    print('End loop 2 at: ', time.ctime())

def main():
    print('Starting at: ', time.ctime())

    t1 = threading.Thread(target=loop1, args=('SmallHong', ))
    t1.start()

    t2 = threading.Thread(target=loop2, args=('SmallHong', 'BigHui'))
    t2.start()

    # 加上join之后，需要等待执行完之后再执行下面的，即等t1和t2都执行完成之后，才会执行最后一句print
    t1.join()
    t2.join()

    print('All done at: ', time.ctime())

if __name__ == '__main__':
    main()
    
'''

'''
# 非守护线程
import time
import threading

def fun():
    print('Start fun')
    time.sleep(2)
    print('End fun')

print('Main thread start')

t1 = threading.Thread(target=fun, args=())
t1.start()

time.sleep(1)
print('Main thread end')
'''

'''
# 守护线程
import time
import threading

def fun():
    print('Start fun')
    time.sleep(2)
    print('End fun')

print('Main thread start')

t1 = threading.Thread(target=fun, args=())
t1.setDaemon(True)
# t1.daemon =  True
t1.start()

time.sleep(1)
print('Main thread end')
'''

'''
import time
import threading

def loop1():
    # ctime 得到当前时间
    print('Start loop 1 at: ', time.ctime())
    time.sleep(4)
    print('End loop 1 at: ', time.ctime())

def loop2():
    print('Start loop 2 at: ', time.ctime())
    time.sleep(2)
    print('End loop 2 at: ', time.ctime())

def loop3():
    print('Start loop 3 at: ', time.ctime())
    time.sleep(5)
    print('End loop 3 at: ', time.ctime())

def main():
    print('Starting at: ', time.ctime())

    t1 = threading.Thread(target=loop1, args=())
    t1.setName('Thread_One')
    t1.start()

    t2 = threading.Thread(target=loop2, args=())
    t2.setName('Thread_Two')
    t2.start()

    t3 = threading.Thread(target=loop3, args=())
    t3.setName('Thread_Three')
    t3.start()

    time.sleep(3)

    for thr in threading.enumerate():
        print('正在运行的线程的名字为: {0}'.format(thr.getName()))

    print('正在运行的子线程数量为: {0}'.format(threading.activeCount()))

if __name__ == '__main__':
    main()

'''

'''
# 线程的继承，普通写法
import threading
import time

class MyThread(threading.Thread):
    def __init__(self, arg):
        super(MyThread, self).__init__()
        self.arg = arg
    def run(self):
        time.sleep(2)
        print('The args for this class is {0}'.format(self.arg))

for i in range(5):
    t = MyThread(i)
    t.start()
    t.join()

print('Main thread is done....')
'''

'''
# 高大上写法，工业写法，工作写法
import threading
from time import sleep, ctime

loop = [4, 2]

class ThreadFunc:
    def __init__(self, name):
        self.name = name

    def loop(self, nloop, nsec):
        # 参数nloop: loop函数的名字, 参数nsec: 休眠时间
        print('Start loop ', nloop, ' at ', ctime())
        sleep(nsec)
        print('Done loop ', nloop, ' at ', ctime())

def main():
    print('Starting at: ', ctime())

    # ThreadFunc('loop').loop 等价于 t = ThreadFunc('loop')   t.loop
    t = ThreadFunc('loop')
    t1 = threading.Thread(target=t.loop, args=('Loop1', 4))
    # 下面这种写法更西方人，工业化一点
    t2 = threading.Thread(target=ThreadFunc('loop').loop, args=('Loop2', 2))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print('All done at: ', ctime())

if __name__ == '__main__':
    main()

'''

'''
import threading

sum = 0
loopSum = 1000000

def myAdd():
    global sum, loopSum
    for i in range(1, loopSum):
        sum += 1

def myMinu():
    global sum, loopSum
    for i in range(1, loopSum):
        sum -= 1

if __name__ == '__main__':

    # myAdd()
    # print(sum)
    # myMinu()
    # print(sum)
    
    # 多线程执行
    t1 = threading.Thread(target=myAdd, args=())
    t2 = threading.Thread(target=myMinu, args=())

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print('Done .... {0}'.format(sum))

    # 注意：因为+或-等操作不是原子操作，因此存在还没有执行完，就使用上一次的变量了
'''

'''
import threading

sum = 0
loopSum = 1000000

lock = threading.Lock() # 申明一把锁

def myAdd():
    global sum, loopSum
    for i in range(1, loopSum):
        # 上锁，申请锁
        lock.acquire()
        sum += 1
        # 释放锁，使用完之后一定要释放锁
        lock.release()

def myMinu():
    global sum, loopSum
    for i in range(1, loopSum):
        lock.acquire()
        sum -= 1
        lock.release()

if __name__ == '__main__':
    print('Starting .... {0}'.format(sum))

    t1 = threading.Thread(target=myAdd, args=())
    t2 = threading.Thread(target=myMinu, args=())

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print('Done .... {0}'.format(sum))
'''

'''
# 生产者消费者模型

import threading
import time

# python2 中的导入: from Queue import Queue
# python3 中的导入: import queue

import queue

# 定义生产者类
class Producer(threading.Thread):
    def run(self):
        global queue
        count = 0
        while True:
            # qsize 返回queue的内容的长度
            if queue.qsize() < 1000:
                for i in range(100):
                    count += 1
                    msg = '生成产品' + str(count)
                    # put是往queue中放入一个值
                    queue.put(msg)
                    print(msg)
            time.sleep(0.5)

# 定义消费者类
class Consumer(threading.Thread):
    def run(self):
        global queue
        while True:
            if queue.qsize() > 100:
                for i in range(3):
                    # get是从queue里面取出一个值
                    msg = self.name + '消费了 ' + queue.get()
                    print(msg)
            time.sleep(1)

if __name__ == '__main__':
    queue = queue.Queue()

    for i in range(500):
        queue.put('初始化产品' + str(i))
    # 生成2个生产者
    for i in range(2):
        p = Producer()
        p.start()
    # 生成5个消费者
    for i in range(5):
        c = Consumer()
        c.start()
        
'''

'''
import threading
import time

lock_1 = threading.Lock()
lock_2 = threading.Lock()

def func_1():
    print('func_1 starting .......')
    lock_1.acquire()
    print('func_1 申请了 lock_1 ......')
    time.sleep(2)
    print('func_1 等待 lock_2 ......')
    lock_2.acquire()
    print('func_1 申请了 lock_2 ......')

    lock_2.release()
    print('func_1 释放了 lock_2')

    lock_1.release()
    print('func_1 释放了 lock_1')

    print('func_1 done ......')


def func_2():
    print('func_2 starting .......')
    lock_2.acquire()
    print('func_2 申请了 lock_2 ......')
    time.sleep(4)
    print('func_2 等待 lock_1 ......')
    lock_1.acquire()
    print('func_2 申请了 lock_1 ......')

    lock_1.release()
    print('func_2 释放了 lock_1')

    lock_2.release()
    print('func_2 释放了 lock_2')

    print('func_2 done ......')


if __name__ == '__main__':
    print('主程序启动 ......')
    t1 = threading.Thread(target=func_1, args=())
    t2 = threading.Thread(target=func_2, args=())

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print('主线程关闭 ......')

'''

'''
# 通过释放锁来解决死锁问题
import threading
import time

lock_1 = threading.Lock()
lock_2 = threading.Lock()

def func_1():
    print('func_1 starting .......')
    rst_1 = lock_1.acquire(timeout=4) # timeout表示最多等待4秒，如果超过了4秒都还没有等到锁，则不等待
    print('func_1 申请了 lock_1 ......')
    time.sleep(2)
    print('func_1 等待 lock_2 ......')
    rst = lock_2.acquire(timeout=2) # 返回值rst为boolean类型，表示申请锁是否成功
    if rst:
        print('func_1 已经得到锁 lock_2')
        lock_2.release()
        print('func_1 释放了锁 lock_2')
    else:
        print('fun_1 没有申请到 lock_2 ......')

    if rst_1:
        lock_1.release()
        print('func_1 释放了 lock_1 ......')

    print('func_1 done ......')

def func_2():
    print('func_2 starting .......')
    lock_2.acquire()
    print('func_2 申请了 lock_2 ......')
    time.sleep(4)
    print('func_2 等待 lock_1 ......')
    lock_1.acquire()
    print('func_2 申请了 lock_1 ......')

    lock_1.release()
    print('func_2 释放了 lock_1')

    lock_2.release()
    print('func_2 释放了 lock_2')

    print('func_2 done ......')

if __name__ == '__main__':
    print('主程序启动 ......')
    t1 = threading.Thread(target=func_1, args=())
    t2 = threading.Thread(target=func_2, args=())

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print('主线程关闭 ......')
    
'''

'''
import threading
import time

# 参数表示最多由几个线程同时使用资源
semaphore = threading.Semaphore(3)

def func():
    if semaphore.acquire():
        for i in range(5):
            print(threading.currentThread().getName() + ' get semaphore')
        time.sleep(15)
        semaphore.release()
        print(threading.currentThread().getName() + ' release semaphore')

# 同时有8个线程同时执行func函数
for i in range(8):
    t1 = threading.Thread(target=func)
    t1.start()
'''

'''
# Timer
import threading
import time

def func():
    print('I am running ......')
    time.sleep(4)
    print('I am done ......')

if __name__ == '__main__':
    # 指定的时间之后调用函数
    t = threading.Timer(6, func)
    t.start()

    i = 0
    while True:
        print('{0} .........'.format(i))
        time.sleep(3)
        i += 1
        
'''

import threading
import time

class MyThread(threading.Thread):
    # 重写父类的run方法
    def run(self):
        global num
        time.sleep(1)

        # 申请锁，最多等待一秒
        if mutex.acquire(1):
            num += 1
            msg = self.name + ' set num to ' + str(num)
            print(msg)
            # 再次申请锁
            mutex.acquire()
            mutex.release()
            mutex.release()

num = 0

mutex = threading.Lock()

def testThread():
    for i in range(5):
        t = MyThread()
        t.start()

if __name__ == '__main__':
    testThread()

'''
import configparser

cfg = configparser.ConfigParser()
'''