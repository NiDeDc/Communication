import socket
import time
import threading


class TcpClient:
    def __init__(self, ip="127.0.0.1", port=7010):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (ip, port)
        self.dataReceive = None
        self.isConnect = False
        t = threading.Thread(target=self.DataReceiveThread, args=(), daemon=True)
        t.start()
        pass

    def RegDataReceiveHandler(self, func):
        self.dataReceive = func

    def ConnectToServer(self, reconnect=True):
        if reconnect:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(self.addr)
            self.isConnect = True
            print("连接服务器成功")
        except socket.error as e:
            print(e)

    def DataReceiveThread(self):
        if not self.isConnect:
            self.ConnectToServer(reconnect=False)
        while True:
            if self.isConnect:
                try:
                    data = self.client.recv(1024)
                    if len(data) > 0:
                        self.dataReceive(data)
                    else:
                        print("服务器断开，等待重连")
                        self.client.close()
                        self.isConnect = False
                except socket.error as e:
                    print(e, "接收数据失败，等待重连")
                    self.client.close()
                    self.isConnect = False
            else:
                time.sleep(1)
                self.ConnectToServer()
