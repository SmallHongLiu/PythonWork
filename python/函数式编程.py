# FunctionalProgramming - 函数式编程，
#   基于lambda演算的一种编程方式
#       程序中只有函数
#       函数可以作为参数，同样可以作为返回值
#       纯函数式编程语言：LISP， Haskell
#   Python函数式编程只是借鉴函数式编程的一些特点，可以理解成一半函数式一半python
#       高级函数
#       返回函数
#       匿名函数
#       装饰器
#       偏函数

# 函数：最大程度复用代码，但是如果函数很小，很短，则会造成啰嗦

# lambda表达式（匿名函数）：一个表达式，函数体相对简单，不是一个代码块，仅仅是一个表达式，可以有参数，有多个参数也可以，用逗号隔开

'''
# 计算一个数字的100倍数，注意这个就是一个表达式，所以没有return
stm = lambda x: 100 * x
# 使用上跟函数调用一摸一样
print(stm(89))

stm2 = lambda x, y, z: x + y * 10 + z * 100
print(stm2(4, 5, 6))

# 高级函数: 将函数作为参数使用的函数，即函数名称就是一个变量
def funA():
    print("In funA")

# funB 和funA只是名称不一样而已
funB = funA
print(funA, funB)
funA()
funB()
'''

'''
def funA(n):
    return n * 100

def funB(n):
    return funA(n) * 3

print(funB(9))

# 高级函数
def funC(n, f):
    return f(n) * 3

print(funC(9, funA))
'''

'''
# 系统高阶函数 - map：具有映射功能，返回值是一个迭代对象
l1 = [i for i in range(10)]
print(l1)
l2 = []
for i in l1:
    l2.append(i * 10)
print(l2)

def mulTen(n):
    return n * 10
l3 = map(mulTen, l1)
print(l3)
'''

'''
# reduce：归并，缩减，把一个可迭代对象最后归并为一个结果，
# 对于作为参数的函数要求：必须有两个参数，必须有返回结果
# reduce([1,2,3,4,5]) = f(f(f(f(1, 2), 3), 4), 5)
# reduce需要导入functools包
from functools import reduce
def myAdd(x, y):
    return x + y

rst = reduce(myAdd, [1, 2, 3, 4, 5, 6])
print(rst)
'''

'''
# filter：过滤函数，对一组数据进行过滤，符合条件的数据会生成一个新的列表返回
# 跟map相比较：
#     相同：都对列表中的每一个元素逐一进行操作
#     不同：map会生成一个跟原来数据相对应的新队列，但是filter不一定，只有符合条件的才会进入新的数据集合
# filter函数怎么写：利用给定函数进行判断，返回值一定是个布尔值，调用格式：filter（f, data), f是过滤函数，data是数据

# 定义一个过滤函数，其中过滤函数必须有输入，返回布尔值
def isEven(a):
    return a % 2 == 0

l = [1, 2, 3, 4, 5, 6, 7, 8, 34]

rst = filter(isEven, l)
print(rst)
print([i for i in rst])
'''

'''
# 高阶函数 - 排序，把一个序列按照给定的算法进行排序, key：在排序中对每一个元素进行key函数运算，可以理解成按照key函数定义的逻辑进行排序
a = [234,  22312, 123,  45, 43, 2, 3, 66723, 34]
al = sorted(a, reverse=False)
print(al)

a = [-43, 23, 45, 6, -23, 2, -4345]
# 按照绝对值排序，key定位为排序的算法函数
al = sorted(a, key = abs, reverse=False)
print(al)

astr = ['dana', 'Dana', 'SmallHong', 'Jingjing', 'haha']
str1 = sorted(astr)
print(str1)

str2 = sorted(astr, key=str.lower)
print(str2)
'''

'''
# 返回函数: 可以返回一个具体的值，也可以返回一个函数作为结果
def myF(a):
    print('In myF')
    return None

a = myF(8)
print(a)

# 注意：函数作为返回值返回时，被返回的函数在函数体内定义
def myF2():
    def myF3():
        print('In myF3')
        return 3
    return myF3

f3 = myF2()
print(f3)
print(f3())

def myF4(*args):
    def myF5():
        rst = 0;
        for n in args:
            rst += n
        return rst
    return myF5
f5 = myF4(1, 2, 3, 4, 5, 6, 7, 8, 9, 0)
print(f5)
print(f5())
'''

'''
# 闭包：当一个函数在内部定义函数，并且内部函数应用外部函数的参数或者局部变量，当内部函数被当作返回值的时候，相关参数和变量保存在返回的函数中，这种结果，就叫闭包
# 上面的myF4是一个标准的闭包结构

def count():
    fs = []
    for i in range(1, 4):
        # f是一个闭包结构的函数
        def f():
            return i * i
        fs.append(f)
    return fs

f1, f2, f3 = count()
# 出现的问题，返回的期望值为1，4， 9，但是返回的实际值为9， 9， 9
# 原因：返回函数引用了变量i, i并非立即执行，而是等到三个函数都返回的时候才统一使用，此时i已经变成了3，最终调用的时候，都返回的是3 * 3
# 因此，返回闭包时，返回函数不能引用任何循环变量
# 解决方案：再创建一个函数，用该函数的参数绑定循环变量的当前值，无论该循环变量以后如何改变，已经绑定的函数参数值不再改变
print(f1(), f2(), f3())

def count1():
    def f(j):
        def g():
            return j * j
        return g
    fs = []
    for i in range(1, 4):
        fs.append(f(i))
    return fs
f1, f2, f3 = count1()
print(f1(), f2(), f3())
'''

'''
# 装饰器：在不改动函数代码的基础上无限扩展函数功能的一种机制，本质上讲，装饰器是一个返回函数的高阶函数
# 装饰器的使用：使用@语法，即在每次要扩展的函数定义前使用@+函数名
def hello():
    print('Hello world')

hello()

f = hello
f()

print(id(f))
print(id(hello))
print(f.__name__)
print(hello.__name__)

#
# 对hello功能进行扩展，每次打印hello之前打印当前系统时间
# 而实现这个功能又不能改动现有代码，故可以使用装饰器
import time
# 定义一个装饰器，使用的时候需要用到@，此符号是python的语法糖
def printTime(f):
    def wrapper(*args, **kwargs):
        print("Time: ", time.ctime())
        return f(*args, **kwargs)
    return wrapper
@printTime
def hello():
    print("hello world")

hello()
# 装饰器的好处：一旦定义，则可以装饰任意函数，一旦被其装饰，则把装饰的功能直接添加到定义的功能上
@printTime
def hello2():
    print("今天很高兴，下午可以好好吃一顿啦")
    print("还可以有很多很多的零食")

hello2()

# 上面对函数的装饰使用了系统定义的语法糖
# 下面开始手动执行装饰器
def hello3():
    print("我是手动执行的")

hello3()
hello3 = printTime(hello3)
hello3()

f = printTime(hello3)
f()
'''

# 偏函数: 参数固定的函数，相当于一个由特定参数的函数体
# 把字符串转换为十进制数字
print(int("12345"))
# 将字符串12345转换为八进制的整数
print(int("12345", base=8))

# 新建一个函数，此函数默认输入的字符串是16进制数字
# 把此字符串返回十进制的数字
def int16(x, base=16):
    return int(x, base)
print(int16("12345"))

# functools.partial的作用是，把一个函数某些参数固定，返回一个新的函数
import functools
int16 = functools.partial(int, base=16)
print(int16("12345"))

