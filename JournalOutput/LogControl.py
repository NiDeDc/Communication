import threading
import datetime
import time
import os


class LogControl:
    def __init__(self, _log_dir='./Log', _size_limit=5, _day_limit=7):
        self.log_dir = _log_dir
        self.size_limit = _size_limit
        self.day_limit = _day_limit
        self.lock = threading.Lock()
        self.log_record = ""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.file_path = os.path.join(self.log_dir, datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S') + ".txt")
        self.WriteTimer()

    def WriteTimer(self):
        if self.log_record != "":
            self.lock.acquire()
            log_file = open(self.file_path, 'a')  # 这里用追加模式，如果文件不存在的话会自动创建
            log_file.write(self.log_record)
            log_file.close()
            self.log_record = ""
            self.SizeJudgment()
            self.lock.release()
        self.DeleteJudgment()
        threading.Timer(5, self.WriteTimer).start()

    def WriteLog(self, content):
        time_format = '%Y-%m-%d %H:%M:%S.%f'  # 指定日期和时间格式
        time_put = datetime.datetime.now().strftime(time_format)  # 格式化时间，时间变成YYYY-MM-DD HH:MI:SS
        log_str = f"{time_put} {content} \n"
        self.lock.acquire()
        self.log_record += log_str
        self.lock.release()

    def SizeJudgment(self):
        file_size = os.path.getsize(self.file_path)
        if file_size > 1024 * 1024 * self.size_limit:
            self.file_path = os.path.join(self.log_dir, datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S') + ".txt")

    def DeleteJudgment(self):
        files = os.listdir(self.log_dir)
        for f in files:
            name = f.split('.')[0]
            try:
                file_time = time.mktime(time.strptime(name, '%Y-%m-%d_%H_%M_%S'))
                if time.time() - file_time > 60 * 60 * 24 * self.day_limit:
                    os.remove(os.path.join(self.log_dir, f))
            except Exception:
                pass
