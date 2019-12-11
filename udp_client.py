import socket

def main(ip:str, port:int, message:str):
    # 实例化对象
    sk = socket.socket(type=socket.SOCK_DGRAM)
    # 定义需要连接的的ip和port
    ip_port = (ip, port)
    # 循环输入数据
    # 输入发送的信息
    msg_input = message
    # 与tcp不同 udp使用sendto函数来发送消息
    sk.sendto(msg_input.encode(), ip_port)
    sk.close()

if __name__ == '__main__':
    main('127.0.0.1', 8888, "hi")