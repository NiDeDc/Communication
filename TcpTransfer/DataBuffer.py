import threading

BUFFER_SIZE = 1 * 1024 * 1024  # 初始缓冲区大小,1M


class DataBuffer:
    def __init__(self):
        self.setSize = BUFFER_SIZE
        self.curSize = 0  # 当前数据大小
        self.dataBuffer = bytearray(self.setSize)
        self.dataLock = threading.Lock()
        print(f"接收缓冲区初始化大小{self.setSize}K")
        pass

    def Rest(self):
        self.dataBuffer = bytearray(self.setSize)
        print(f"接收缓冲区重置大小{self.setSize}byte")

    def ResizeBuffer(self, size):
        while self.setSize < size:
            self.setSize *= 2
        old_data: bytearray = self.dataBuffer.copy()
        self.Rest()
        self.dataBuffer[0: self.curSize] = old_data[:]

    def AddData(self, byteAry: bytearray):
        new_len = len(byteAry)
        size = self.curSize + new_len
        self.dataLock.acquire()
        if size > self.setSize:
            self.ResizeBuffer(size)
        else:
            pass
        self.dataBuffer[self.curSize: size] = byteAry[:]
        self.curSize = size
        self.dataLock.release()

    def PollData(self, size):
        if size > self.curSize:
            return None
        data = self.dataBuffer[: size].copy()
        self.dataLock.acquire()
        self.dataBuffer[:self.curSize - size] = self.dataBuffer[size: self.curSize]
        self.curSize -= size
        self.dataLock.release()
        return data

    def PollDataByEdge(self, size, edge: bytearray):  # 通过起始边界寻找数据
        edge_size = len(edge)
        for i in range(self.curSize - 1):
            if self.dataBuffer[i:i + edge_size] == edge:
                if i == 0:
                    return self.PollData(size)
                else:
                    self.PollData(i)
                    return self.PollData(size)
            else:
                continue
        return None
