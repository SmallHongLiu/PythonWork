# 装饰器

from functools import wraps

def a_new_decorator(a_func):
    @wraps(a_func)
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func")
        a_func()
        print("I am doing some boring work after executing a_func")
    return wrapTheFunction

@a_new_decorator
def a_function_requiring_decoration():
    print("I am the function which needs some decoration to remove my foul smell")

print(a_function_requiring_decoration.__name__)

# 装饰器授权
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authoriztion
        if not auth or not check_auth(auth.username, auth.password):
            authenticate()
        return f(*args, **kwargs)
    return decorated

# 装饰器日志
def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + " was called")
        return func(*args, **kwargs)
    return with_logging

@logit
def addition_func(x):
    return x + x

result = addition_func(4)

# 函数中嵌入装饰器
def logit(logfile='out.log'):
    def logging_decorator(func):
        @wraps(func)
        def wrapper_function(*args, **kwargs):
            log_string = func.__name__ + " was called"
            print(log_string)
            # 打开logfile, 并写入内容
            with open(logfile, 'a') as opened_file:
                # 现在将日志打到指定的logfile
                opened_file.write(log_string + "\n")
            return func(*args, **kwargs)
        return wrapper_function
    return logging_decorator

@logit()
def myfunc1():
    pass

myfunc1()

@logit(logfile='func2.log')
def myfunc2():
    pass

myfunc2()

# 类装饰器
class logit(object):
    def __init__(self, logfile='out.log'):
        self.logfile = logfile

    def __call__(self, func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = func.__name__ + " was called"
            print(log_string)
            # 打开logfile 并写入
            with open(self.logfile, 'a') as opened_file:
                # 现在将日志打到指定的文件
                opened_file.write(log_string + "\n")
            # 现在，发送一个通知
            self.notify()
            return func(*args, **kwargs)
        return wrapped_function

    def notify(self):
        # logit 只打印日志，不做别的
        pass

@logit()
def myfunc1():
    pass

# 创建logit子类
class email_logit(logit):
    '''一个logit的实现版本，可以在函数调用时发送email给管理员'''
    def __init__(self, email='admin@myproject.com', *args, **kwargs):
        self.email = email
        super(logit, self).__init__(*args, **kwargs)

    def notify(self):
        # 发送一封email到self.email
        pass

# return
def add(value1, value2):
    return value1 + value2

result = add(3, 5)
print(result)

def add(value1, value2):
    global result
    result = value1 + value2

add(2, 4)
print(result)

'''返回多个值'''
# 方式1: 返回一个包含多个值的tuple，list或dict
def profile():
    name = "Danny"
    age = 30
    return (name, age)
    # return name, age

profile_data = profile()
print(profile_data[0])

print(profile_data[1])

# 对象变动 Mutation
def add_to(num, target=[]):
    target.append(num)
    return target

add_to(1)

add_to(2)

add_to(3)

def add_to(element, target=None):
    if target is None:
        target = []
    target.append(element)
    return target

# 使用或不使用__slots__
class MyClass(object):
    def __init__(self, name, identifier):
        self.name = name
        self.identifier = identifier
        self.set_up()

class MyClass(object):
    __slots__ = ['name', 'identifier']  # 使用slots可以有效的减轻内存负担
    def __init__(self, name, identifier):
        self.name = name
        self.identifier = identifier
        self.set_up()

'''容器Collections'''
# defaultdict
from collections import defaultdict
colours = (
    ('Yasoob', 'Yellow'),
    ('Ali', 'Blue'),
    ('Arham', 'Green'),
    ('Ali', 'Black'),
    ('Yasoob', 'Red'),
    ('Ahemd', 'Silver'),
)

favourite_colours = defaultdict(list)

for name, colour in colours:
    favourite_colours[name].append(colour)

print(favourite_colours)

# 避免KeyError
import collections
tree = lambda: collections.defaultdict(tree)
some_dict = tree()
some_dict['colours']['favourite'] = 'yellow'

import json
print(json.dumps(some_dict))

# Counter 计数器
from collections import Counter

favs = Counter(name for name, colour in colours)
print(favs)
# 统计文件
with open('filename', 'rb') as f:
    line_count = Counter(f)
print(line_count)

# deque双端队列
from collections import deque

d = deque()

d.append('1')
d.append('2')
d.append('3')

print(len(d))
print(d[0])
print(d[-1])

d = deque(range(5))
print(len(d))

d.popleft()
d.pop()
print(d)

# 设置限制，超出时，另一端被挤出
d = deque(maxlen=30)
d = deque([1, 2, 3, 4, 5])
d.extendleft([0])
d.extend([6, 7, 8])
print(d)

'''namedtuple'''
man = ('Ali', 30)
print(man[0])

from collections import namedtuple

Animal = namedtuple('Animal', 'name age type')
perry = Animal(name='perry', age=31, type='cat')

print(perry)

# 不可变
from collections import namedtuple

Animal = namedtuple('Animal', 'name age type')
perry = Animal(name='Perry', age=31, type='cat')
perry.age = 12  # 属性值不可变

# namedtuple转换为dict
print(perry._asdict())


'''enum.Enum 枚举'''
from collections import namedtuple
from enum import Enum

class Species(Enum):
    cat = 1
    dog = 2
    horse = 3
    aardvark = 4
    butterfly = 5
    owl = 6
    platypus = 7
    dragon = 8
    unicorn = 9

    kitten = 1
    puppy = 2

Animal = namedtuple('Animal', 'name age type')
perry = Animal(name='Perry', age=31, type=Species.cat)
dragon = Animal(name='Drogon', age=4, type=Species.dragon)
tom = Animal(name='Tom', age=75, type=Species.cat)
charlie = Animal(name='Charlie', age=2, type=Species.kitten)

print(charlie.type)
print(charlie.type == tom.type)

'''枚举函数Enumerate'''
for counter, value in enumerate(some_list):
    print(counter, value)

my_list = ['apple', 'banana', 'grapes', 'pear']
for c, value in enumerate(my_list, 1):
    print(c, value)

counter_list = list(enumerate(my_list, 1))
print(counter_list)

'''对象自省 introspection  dir'''
my_list = [1, 2, 3]
dir(my_list)

# type返回一个对象的类型
print(type(''))
print(type([]))
print(type({}))
print(type(dict))
print(type(3))

# id返回任意不同种类对象的唯一id
name = 'Yasoob'
print(id(name))

'''inspect模块'''
import inspect
print(inspect.getmembers(str))

'''推导式Comprehension'''
# 列表推导式
multiples = [i for i in range(30) if i % 3 is 0]
print(multiples)

# 列表推导式的简化
# 普通
squared = []
for x in range(10):
    squared.append(x ** 2)
# 列表推导式简化形式
squared = [x ** 2 for x in range(10)]

# 字典推导式
mcase = {'a': 10, 'b': 34, 'A': 7, 'Z': 3}
mcase_frequency = {
    k.lower(): mcase.get(k.lower, 0) + mcase.get(k.upper(), 0)
    for k in mcase.keys()
}

# 快速对换一个字典的键和值
{v: k for k, v in some_dict.items()}

# 集合推导式(set comprehensions)
squared = {x ** 2 for x in [1, 1, 2]}
print(squared)

'''异常'''
# 处理单个异常
try:
    file = open('test.txt', 'rb')
except IOError as e:
    print('An IOError occurred. {}'.format(e.args[-1]))
# 处理多个异常
try:
    file = open('test.txt', 'rb')
except EOFError as e:
    raise e
except IOError as e:
    print('An error occurred.')
    raise e
# 文件的方式捕获异常
try:
    file = open('test.txt', 'rb')
except Exception:
    raise

# finally从句
try:
    file = open('test.txt', 'rb')
except IOError as e:
    print('An IOError occurred. {}'.format(e.args[-1]))
finally:
    print('This would be printed whether or not an exception occurred!')

# try／else从句
try:
    print('I am sure no excception is going to occur!')
except Exception:
    print('exception')
else:
    # 这里的代码只会在try语句里没有触发异常时运行，但是这里的异常将不会被捕获
    print('This would only run if no exception occurs. And an error would NOT be caught.')
finally:
    print('This would be printed in every case.')

'''lambda 表达式'''
add = lambda x, y: x + y
print(add(3, 5))

# 列表排序
a = [(1, 2), (4, 1), (9, 10), (13, -3)]
a.sort(key=lambda x: x[1])
print(a)

# 列表并行排序
data = zip(list1, list2)
data.sort()
list1, list2 = map(lambda t: list(t), zip(*data))

'''一行式'''
# 打印
from pprint import pprint
my_dict = {'name': 'Yassob', 'age': 'undefined', 'personality': 'true'}
pprint(my_dict)

# 列表辗平
import itertools
a_list = [[1, 2], [3, 4], [5, 6]]
print(list(itertools.chain.from_iterable(a_list)))
print(list(itertools.chain(*a_list)))

# 一行式构造器
class A(object):
    def __init__(self, a, b, c, d, e, f):
        self.__dict__.update({k: v for k, v in locals().items()})

'''For - Else'''
fruits = ['apple', 'banana', 'mango']
for fruit in fruits:
    print(fruit.capitalize())

for item in container:
    if search_something(item):
        process(item)
        break
else:
    # Didn't find anyting...
    not_found_in_container()

'''使用C扩展'''
# CTypes模块
from ctypes import *

# load the shared object file
adder = CDLL('./adder.so')

# Find sum of integers
res_int = adder.add_int(4, 5)
print('Sum of 4 and 5 = ', str(res_int))

# Find sum of floats
a = c_float(5.5)
b = c_float(4.1)

add_float = adder.add_float
add_float.restype = c_float
print("Sum of 5.5 and 4.1 = ", str(add_float(a, b)))

# open 函数
f = open('photo.jpg', 'r+')
jpg_data = f.read()
f.close()

with open('photo.jpg', 'r+') as f:
    jpg_data = f.read()

import io

with open('photo.jpg', 'rb') as inf:
    jpg_data = inf.read()

if jpg_data.startswith(b'\xff\xd8'):
    text = u'This is a JPEG file (%d bytes long)\n'
else:
    text = u'This is a random file (%d bytes long)\n'

with io.open('summary.txt', 'w', encoding='utf-8') as outf:
    outf.write(text % len(jpg_data))

# Future模块
from __future__ import with_statement

from __future__ import print_function
print(print)

# 模块重命名
try:
    import urllib.request as urllib_request # for python 3
except ImportError:
    import urllib2 as urllib_request # for python 2

# 生成器
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# grep的实现
def grep(pattern):
    print("Searching for", pattern)
    while True:
        line = (yield)
        if pattern in line:
            print(line)

'''函数缓存'''
# lru_cache装饰器
from functools import lru_cache

@lru_cache(maxsize=32)  # 设置最多缓存最近的多少个返回值
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
print([fib(n) for n in range(10)])

fib.cache_clear() # 清空缓存的返回值

'''基于类的实现'''
class File(object):
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)
    def __enter__(self):
        return self.file_obj
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_obj.close()

with File('demo.txt', 'w') as opened_file:
    opened_file.write("Hola!")

'''处理异常'''
class File(object):
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)
    def __enter__(self):
        return self.file_obj
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exception has been handled")
        self.file_obj.close()
        return True  # 返回true，因此没有异常会被with语句抛出

with File('demo.txt', 'w') as opened_file:
    opened_file.write("Hola!")


'''基于生成器的实现'''
from contextlib import contextmanager

@contextmanager
def open_file(name):
    f = open(name, 'w')
    yield f
    f.close()
