"""
加载器的基类
这是一个抽象类，原则是所有的加载器（xxxLoader.py）都应该继承这个类
要求实现一个 run 方法
"""
from abc import ABC, abstractmethod


class BaseLoader(ABC):
    @abstractmethod
    def run(self):
        pass
