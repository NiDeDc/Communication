from DataBuffer import DataBuffer
import struct
import json
import time


class PacketHead:
    def __init__(self):
        self.head = 0
        self.reserve = 0
        self.type = 0
        self.msgId = 0
        self.dataLen = 0


class PacketModel:
    def __init__(self):
        self.buffer = DataBuffer()
        self.headFormat1 = '3H'
        self.headFormat2 = '2I'
        self.packetHeadLen = struct.calcsize(self.headFormat1) + struct.calcsize(self.headFormat2)

    def AddDataToBuffer(self, data):
        self.buffer.AddData(data)

    def UnpackData(self):
        # data = self.buffer.PollData(self.packetHeadLen)
        data = self.buffer.PollDataByEdge(self.packetHeadLen, bytearray([0xFC, 0xFc]))
        if data is None:
            return False
        else:
            pack1 = struct.unpack_from(self.headFormat1, data[:6])
            pack2 = struct.unpack_from(self.headFormat2, data[6:])
            a = pack1 + pack2
            packt_head = PacketHead()
            head_dict = packt_head.__dict__
            index = 0
            for i in head_dict.keys():
                head_dict[i] = a[index]
                index += 1
            if packt_head.head != 0xFCFC:
                print("包头错误")
                return False
            remain_len = packt_head.dataLen + 2
            wait_time = time.time()
            remain_data = self.buffer.PollData(remain_len)
            while remain_data is None:
                if time.time() - wait_time < 5:
                    remain_data = self.buffer.PollData(remain_len)
                else:
                    print("等待包体超时,等待解包")
                    return False
            end = struct.unpack_from('H', remain_data[-2:])[0]
            if end != 0xFDFD:
                print("包尾错误")
                return False
            if packt_head.type == 1:
                json_data = json.loads(remain_data[0: -2])
                print(json_data)
                return json_data
