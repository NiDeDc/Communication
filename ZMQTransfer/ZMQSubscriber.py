import zmq
import threading


class MessageSubscriber:
    def __init__(self, ip='127.0.0.1', port='8010', theme: bytes = bytes(''.encode('utf-8')), timeout=1000, sub_id=0):
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        self.theme = theme
        self.address = "tcp://{}:{}".format(ip, port)
        self.subscriber.setsockopt(zmq.RCVTIMEO, timeout)
        self.subscriber.setsockopt(zmq.TCP_KEEPALIVE, 1)
        self.subscriber.setsockopt(zmq.TCP_KEEPALIVE_IDLE, 2)
        self.subscriber.setsockopt(zmq.TCP_KEEPALIVE_CNT, 2)
        self.subscriber.connect(self.address)
        self.subscriber.setsockopt(zmq.SUBSCRIBE, theme)
        self.dataReceive = None
        self.sub_id = sub_id
        t = threading.Thread(target=self.ReceiveThread, args=(), daemon=True)
        t.start()

    def RegDataReceiveHandler(self, func):
        self.dataReceive = func

    def ReceiveThread(self):
        while True:
            try:
                message = self.subscriber.recv()
                if self.dataReceive is not None:
                    self.dataReceive(message)
                # print(message)
            except zmq.ZMQError as e:
                print(f"订阅{self.sub_id}接收数据超时")
