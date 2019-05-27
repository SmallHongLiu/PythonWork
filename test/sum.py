# coding=utf-8
'''
Author: Small_Hong
date: 2019-05-20 $ {TIME}
'''

# 在这里我们将上面文件定义的param中的g作为重力参数引入到其中
from param import g


def calc_G(m):
    G = m * g
    return G


def main():
    print('G: ', calc_G(10))


main()
