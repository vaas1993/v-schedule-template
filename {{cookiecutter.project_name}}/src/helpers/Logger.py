import datetime
import inspect
import os.path
import const

"""
统一日志打印类
原则是程序所有对终端的输出都可以使用这个类来控制
实现了一个简单的日志等级，可通过配置文件来设置需要的输出
"""


class Logger:
    # 日志文件
    log_file = None

    # 日志等级
    levels = {
        "DEBUG": 0,
        "INFO": 1,
        "SUCCESS": 2,
        "WARN": 3,
        "ERR": 4,
        "LOG": 5,
    }

    def __init__(self):
        """
        构造函数
        """
        # 打印等级
        self.level = 1
        if const.ENV_PRODUCTION:
            self.level = 4
        if const.ENV_PREVIEW:
            self.level = 3
        if const.ENV_TEST:
            self.level = 2
        if const.ENV_DEVELOPMENT:
            self.level = 0
        self.level = 0 if const.DEBUG else self.level

    def get_log_file(self):
        """
        获取日志文件句柄
        :return:
        """
        date = datetime.datetime.now().strftime("%Y%m%d")
        path = f"runtime/logs/{date}.log"
        if self.log_file is None:
            self.log_file = open(file=path, mode="a")
        if not os.path.exists(path) or self.log_file.name != path:
            self.log_file.close()
            self.log_file = open(file=path, mode="a")
        return self.log_file

    def _print(self, message: str, level: str):
        """
        打印的实现方法
        :param message: 需要打印的日志消息
        :param level: 打印等级
        """
        if self.levels.get(level, 0) < self.level:
            return
        color = "0m"
        if level == "SUCCESS":
            color = "32m"
        if level == "WARN":
            color = "33m"
        if level == "ERR":
            color = "31m"

        frame = inspect.getouterframes(inspect.currentframe(), 2)[2]
        target = os.path.relpath(frame.filename)
        line = frame.lineno

        msg = "".join([
            f'[{level}]',
            f'[{target}]',
            f'[Line {line}]',
            f'[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ']',
            ' ',
            message,
        ])

        # 对于 err 和 warn 等级的，记录到日志文件
        if level in ["ERR", "WARN"]:
            self.get_log_file()
            self.log_file.write(msg + "\n")
            self.log_file.flush()

        # 除了预发布和正式环境，其它环境增加打印样式
        if not (const.ENV_PRODUCTION or const.ENV_PREVIEW):
            msg = "".join([
                "\033[",
                color,
                f'[{level}]',
                f'[{target}]',
                f'[Line {line}]',
                f'[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ']',
                ' ',
                message,
                '\033[0m',
            ])

        print(msg)

    def debug(self, message: str):
        """
        打印 INFO 级别的消息
        :param message: 需要打印的日志消息
        """
        self._print(message=message, level="DEBUG")

    def log(self, message: str):
        """
        打印 LOG 级别的消息
        :param message: 需要打印的日志消息
        """
        self._print(message=message, level="LOG")

    def info(self, message: str):
        """
        打印 LOG 级别的消息
        :param message: 需要打印的日志消息
        """
        self._print(message=message, level="INFO")

    def success(self, message: str):
        """
        打印 SUCCESS 级别的消息
        :param message: 需要打印的日志消息
        """
        self._print(message=message, level="SUCCESS")

    def warn(self, message: str):
        """
        打印 WARN 级别的消息
        :param message: 需要打印的日志消息
        """
        self._print(message=message, level="WARN")

    def err(self, message: str):
        """
        打印 ERR 级别的消息
        :param message: 需要打印的日志消息
        """
        self._print(message=message, level="ERR")
