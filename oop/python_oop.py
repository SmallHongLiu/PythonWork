'''
定义一个学生类，用来形容学生
'''

'''
# 定义一个空的类
class Student():
    # 一个空类，pass代表直接跳过
    # 此处pass必须有，因为类下面必有内容，如果没有，则必须加上pass
    pass

# 定义一个对象
small_hong = Student()

# 定义一个类，用来描述听Python的学生
class PythonStudent():
    # 用None给不确定值的变量赋值
    name = None
    age = 18
    course = "Python"

    # 缩进层级
    # 默认的self参数
    def doHomework(self):
        print("do homework")
        # 推荐在函数末尾使用return语句，但也可以不写
        return None

# 实例化一个对象
studentOne = PythonStudent()
print(studentOne.name)
print(studentOne.age)
# 注意成员函数的调用没有传递参数®
studentOne.doHomework()
'''

'''
class A():
    pass
class B(A):
    pass

class C(B, A):
    pass

print(A.__mro__)
print(B.__mro__)
'''

'''多继承，子类可以直接拥有父类'''
'''
class Fish():
    def __init__(self, name):
        self.name = name
    def swim(self):
        print("I am swimming....")

class Bird():
    def __init__(self, name):
        self.name = name
    def fly(self):
        print("I am flying...")

class Person():
    def __init__(self, name):
        self.name = name
    def work(self):
        print("I am working...")

# 继承是有顺序的，从左到右
class SuperMan(Person, Bird, Fish):
    def __init__(self, name):
        self.name = name
    pass

class Student(Person):
    def __init__(self, name):
        self.name = name

s = SuperMan("Small_Hong")
s.fly()
s.swim()
'''

'''
# 子类扩展父类的构造函数
class A():
    def __init__(self):
        print("A")

class B(A):
    def __init__(self, name):
        print("B")
        print(name)

class C(B):
    # c中扩展B的构造函数，即调用B的构造函数后再添加一些功能
    # 第一种实现：通过父类名调用
    # def __init__(self, name):
    #     B.__init__(self, name)
    #     print("这是C中附加的功能")

    # 第二种实现：通过super调用
    def __init__(self, name):
        super(C, self).__init__(name)
        print("这是C中附加的功能")

c = C("我是C")
'''

'''
class Person():
    name = "Small_Hong"
    age = 18

    def eat(self):
        print("eat...")
    def drink(self):
        print("drink...")
    def sleep(self):
        print("sleep...")

class Teacher(Person):
    def work(self):
        print("work...")

class Student(Person):
    def study(self):
        print("study...")

class Tutor(Teacher, Student):
    pass

t = Tutor()
# 打印MRO列表
print(Tutor.__mro__)
print(t.__dict__)
print(Tutor.__dict__)

print("*" * 20)

class TeacherMixin():
    def work(self):
        print("work")

class StudentMixin:
    def study(self):
        print("study")

class TutorM(Person, TeacherMixin, StudentMixin):
    pass

tm = TutorM()
print(TutorM.__mro__)
print(tm.__dict__)
print(TutorM.__dict__)
'''

help(setattr)



