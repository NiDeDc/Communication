from ZMQSubscriber import MessageSubscriber
from InsAgreement import PacketModel
from JournalOutput.LogControl import LogControl
import time
import csv


def ReadEdge():
    ip_config = []
    filename = 'EdgeIpSheet.csv'
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 3:
                ip_config.append([row[0], row[2], row[3]])
    return ip_config


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    IP = ReadEdge()
    mesSubs = []
    packet = PacketModel()
    for i in range(len(IP)):
        MesSub = MessageSubscriber(port=IP[i][2],  ip=IP[i][1], theme=bytes('FL'.encode('utf-8')), sub_id=IP[i][0])
        MesSub.RegDataReceiveHandler(packet.UnpackData)
        mesSubs.append(mesSubs)
    timeLog = LogControl()
    while True:
        pack = packet.Dequeue()
        if pack.dev != -1:
            strLog = f"dev:{pack.dev}, ch:{pack.ch}, timestamp:{pack.datatime}"
            print(strLog)
            timeLog.WriteLog(strLog)
        else:
            time.sleep(0.1)

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
