from TcpClient import TcpClient
from MetroAgreement import *
from JournalOutput.LogControl import LogControl
from GlobalShared import TcpConfig as cfg
import time


# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    Packt = PacketModel()
    ip = cfg.read_config('TCPCLIENT', 'ip')
    port = int(cfg.read_config('TCPCLIENT', 'port'))
    client = TcpClient(ip=ip, port=port)
    client.RegDataReceiveHandler(Packt.AddDataToBuffer)
    preAlarmLog = LogControl(_log_dir='./preAlarmLog', _size_limit=5, _day_limit=14)
    alarmLog = LogControl(_log_dir='./alarmLog', _size_limit=5, _day_limit=60)
    trainLog = LogControl(_log_dir='./trainLog', _size_limit=5, _day_limit=7)
    usageLog = LogControl(_log_dir='./usageLog', _size_limit=5, _day_limit=60)
    queueStackLog = LogControl(_log_dir='./queueStackLog', _size_limit=5, _day_limit=60)
    offOnlineLog = LogControl(_log_dir='./offOnlineLog', _size_limit=5, _day_limit=60)
    fiberCutLog = LogControl(_log_dir='./fiberCutLog', _size_limit=5, _day_limit=180)
    while True:
        data = Packt.UnpackData()
        if not data:
            time.sleep(0.1)
        else:
            cmd = data['cmd']
            if cmd == 2:
                preAlarmLog.WriteLog(data)
            elif cmd == 3:
                alarmLog.WriteLog(data)
            elif cmd == 4:
                trainLog.WriteLog(data)
            elif cmd == 5:
                usageLog.WriteLog(data)
            elif cmd == 6:
                queueStackLog.WriteLog(data)
            elif cmd == 7:
                offOnlineLog.WriteLog(data)
            elif cmd == 8:
                fiberCutLog.WriteLog(data)


# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
