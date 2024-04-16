from _decimal import Decimal

"""
数学类
封装常用数学计算
"""


class Math:

    @staticmethod
    def round(number: float, fixed=2):
        """
        四舍五入，解决某些情况下精度丢失的问题
        :param number: 待处理的浮点数
        :param fixed: 需要保留的小数位
        :return:
        """
        return round(Decimal(number), fixed)
