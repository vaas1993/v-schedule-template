import abc
from abc import ABC

from config import main


class BaseOpen(ABC):
    def __init__(self):
        self.response = None
        self.params = {}
        self.config = None

    def runnable(self):
        if self.before_run():
            self.response = self.run()
            self.after_run()

    @abc.abstractmethod
    def get_config_name(self) -> str:
        """
        获取配置名称
        需要在主配置文件中的 open_config 内定义
        :return:
        """
        pass

    def get_config_item(self, name: str, default=None):
        """
        获取配置项
        :param name: 配置项名称
        :param default: 当配置项不存在时返回的默认值
        :return:
        """
        if self.config is None:
            self.config = main.config["open_config"][self.get_config_name()]
        return self.config[name] if name in self.config else default

    def before_run(self) -> bool:
        """
        主函数运行前的钩子，返回 False 可阻止主函数运行
        :return:
        """
        return True

    def after_run(self):
        """
        主函数运行后的钩子
        用于处理运行完成后的收尾工作
        :return:
        """
        pass

    def set_params(self, params: dict):
        """
        设置参数
        :param params: dict
        :return:
        """
        self.params = params

    @abc.abstractmethod
    def run(self) -> dict:
        """
        主函数，由子类实现
        :return: dict 返回接口请求的响应数据
        """
        pass

    @abc.abstractmethod
    def get_is_success(self) -> bool:
        """
        判断当前请求是否成功
        :return:
        """
        pass

    @abc.abstractmethod
    def get_message(self) -> str:
        """
        获取请求结果的消息描述
        :return:
        """
        pass
