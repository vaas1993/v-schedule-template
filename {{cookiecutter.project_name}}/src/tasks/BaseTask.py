import abc

"""
任务基类
所有任务都应该继承该类或者该类的子类，否则无法运行

程序实例化任务类后，会运行 runnable 方法，该方法包含了一个简易的钩子逻辑运算
"""


class BaseTask(abc.ABC):
    def __init__(self):
        # 任务参数
        self.params = {}

    def set_params(self, params: dict):
        """
        设置任务参数
        :param params:
        :return:
        """
        self.params = params

    async def runnable(self):
        if self.before_run():
            await self.run()
            self.after_run()

    def before_run(self) -> bool:
        """
        主函数运行前的钩子，返回 False 可阻止主函数运行
        :return:
        """
        return True

    def after_run(self):
        """
        主函数运行后的钩子
        用于处理任务运行完成后的收尾工作
        :return:
        """
        pass

    @abc.abstractmethod
    async def run(self):
        """
        任务运行的主函数，由子类实现
        :return:
        """
        pass
