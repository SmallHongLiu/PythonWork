# 一个学生类
class Student():
    def __init__(self, name="NoName", age=18):
        self.name = name
        self.age = age

    def say(self):
        print("My name is {0}".format(self.name))


def sayHello():
    print("Hi, 欢迎来到图灵学院!")

# 此判断语句建议一直作为程序的入口
if __name__ == "__mani__":
    print("我是模块，你好")