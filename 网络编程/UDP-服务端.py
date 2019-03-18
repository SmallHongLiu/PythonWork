# 模拟服务器的函数
import socket

def serverFunc():

    # 1.建立socket
    # socket.AF_INET：使用ipv4协议族
    # socket.SOCK_DGRAM：使用UDP通信
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 2. 绑定ip和port
    # 127.0.0.1: 这个IP地址代表机器本身
    # 7852: 随便指定
    # 地址是一个tuple类型（ip, port)
    addr = ('127.0.0.1', 7852)
    sock.bind(addr)

    # 接受对方消息
    # 等待方式为死等，没有其它可能性
    # recvfrom接受的返回值是一个元祖tuple, 前一项表示数据，后一项表示地址
    # 参数的含义是缓冲区大小
    # rst = sock.recvfrom(500)
    data, addr = sock.recvfrom(500)

    print(data)
    print(type(data))

    # 发送过来的数据是bytes格式，必须通过解码才能得到str格式内容
    # decode默认参数是utf-8
    text = data.decode()
    print(type(text))
    print(text)

    # 给对方返回的消息
    rsp = 'Ich hab keine Hunge'

    # 发送的数据需要编码成bytes格式
    # 默认是utf-8
    data = rsp.encode()
    sock.sendto(data, addr)

if __name__ == '__main__':
    print('Starting server.....')
    serverFunc()
    print('Done server......')

    '''
    为了让服务器不自动挂掉，此处采用死循环的方式
    import time
    while True:
        try:
            serverFunc()
        except Exception as e:
            print(e)
            
        time.sleep(1
    '''


