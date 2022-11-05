import struct
from queue import Queue


class PacketHead:
    def __init__(self):
        self.theme: bytes = ''.encode('utf-8')
        self.datatime = 0
        self.type = 0
        self.dev = -1
        self.ch = 0
        self.colum = 0


class PacketModel:
    def __init__(self):
        self.headFormat1 = '2s'
        self.headFormat2 = 'Q4H'
        self.packetHeadLen = struct.calcsize(self.headFormat1) + struct.calcsize(self.headFormat2)
        # print(self.packetHeadLen)
        self.q = Queue(maxsize=1000)

    def UnpackData(self, data: bytes):
        pack1 = struct.unpack_from(self.headFormat1, data[:2])
        pack2 = struct.unpack_from(self.headFormat2, data[2:self.packetHeadLen])
        a = pack1 + pack2
        packt_head = PacketHead()
        head_dict = packt_head.__dict__
        index = 0
        for i in head_dict.keys():
            head_dict[i] = a[index]
            index += 1
        if packt_head.theme.decode() == 'FL':
            self.Enqueue(packt_head)

    def Enqueue(self, block: PacketHead):
        if self.q.full():
            self.q.get()
        self.q.put(block)

    def Dequeue(self) -> PacketHead:
        if self.q.empty():
            return PacketHead()
        else:
            return self.q.get()
