import socket
def main(ip:str, port:int):
    # 创建实例  并指定udp参数
    sk = socket.socket(type=socket.SOCK_DGRAM)
    # 定义绑定的ip和port
    ip_port = (ip, port)
    # 绑定监听
    sk.bind(ip_port)
    print("is receiving signal")
    # 循环接收数据
    while True:
        # 接收数据
        data = sk.recv(1024)
        # 打印数据
        print("receive {}".format(data.decode()))
        if data=='exit':
            break
    print("udp_server exit successfully")