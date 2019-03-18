import socket
def tcp_srv():
    # 1. 建立socket负责具体通信，这个socket其实只是负责接受对方的请求，真正通信的是链接后
    # 需要用到两个参数
    # AF_INET：含有同UDP一样
    # SOCK_STREAM：表明是使用tcp进行通信
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 2. 绑定端口和地址
    # 此地址信息是一个元组类型内容，元组分为两部分，第一部分为字符串，代表ip，第二部分为端口
    addr = ('127.0.0.1', 8998)
    sock.bind(addr)
    # 3. 监听接入的访问socket
    sock.listen()

    while True:
        # 4. 接受访问的socket，可以理解接受访问即建立一个通信的链接通路
        # accept返回的元组第一个元素赋值给skt，第二个赋值给addr
        skt, addr = sock.accept()
        # 5. 接受对方的发送内容，利用接收到的socket接受内容
        # 500代表接收使用的缓存buffer大小
        # msg = skt.receive(500)
        msg = skt.recv(500)
        # 接受到的是bytes格式内容
        # 想得到str格式，需要进行解码
        msg = msg.decode()

        rst = 'Received msg: {0} from {1}'.format(msg, addr)
        print(rst)
        # 6. 如果有必要，给对方发送反馈信息
        skt.send(rst.encode())

        # 7. 关闭链接通路
        skt.close()

if __name__ == '__main__':
    print('Starting tcp server ......')
    tcp_srv()
    print('Done tcp server ......')
