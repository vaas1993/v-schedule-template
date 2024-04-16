"""
封装常用的日期时间方法
"""


class Moment:

    @staticmethod
    def sec_to_text(seconds: int) -> str:
        """
        将秒数格式化成 x年x月x日x小时x分钟x秒 的格式
        :param seconds: int 秒
        :return: str
        """
        # 计算年、月、日、小时、分钟和秒
        years = seconds // (365.25 * 24 * 3600)
        seconds %= (365.25 * 24 * 3600)
        months = seconds // (30 * 24 * 3600)
        seconds %= (30 * 24 * 3600)
        days = seconds // (24 * 3600)
        seconds %= (24 * 3600)
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        result = []
        if years:
            result.append(f"{int(years)}年")
        if months:
            result.append(f"{int(months)}月")
        if days:
            result.append(f"{int(days)}天")
        if hours:
            result.append(f"{int(hours)}小时")
        if minutes:
            result.append(f"{int(minutes)}分钟")
        if seconds:
            result.append(f"{int(seconds)}秒")
        return "".join(result)
