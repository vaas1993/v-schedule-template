import abc
import os.path
import random
from abc import ABC
from datetime import datetime

from src.helpers.Email import Email
from src.helpers.Math import Math
from src.tasks.BaseTask import BaseTask
import dominate.tags

"""
实现了发送邮件的任务基类
如果任务需要用到邮件发送则可以选择继承该类
"""


class BaseEmailSenderTask(BaseTask, ABC):
    def __init__(self):
        super().__init__()
        self.email_attachments = []

    def send_email(self) -> bool:
        """
        发送邮件
        :return: bool
        """
        email = Email()
        email.set_subject(self.get_email_subject())
        email.set_receivers(self.get_email_receivers())
        email.set_ccs(self.get_email_ccs())
        email.set_content(self.get_email_content())
        for item in self.email_attachments:
            email.add_attachment(path=item["path"], name=item["name"])
        return email.send(sender=self.get_email_sender())

    def add_email_attachment(self, path: str, name: str):
        """
        添加附件
        :param path: 文件路径
        :param name: 附件名称
        :return:
        """
        self.email_attachments.append({
            "path": path,
            "name": name
        })

    @abc.abstractmethod
    def get_email_content(self) -> str:
        return ""

    @abc.abstractmethod
    def get_email_subject(self) -> str:
        return ""

    @abc.abstractmethod
    def get_email_receivers(self) -> list:
        return []

    def get_email_ccs(self) -> list:
        return []

    @staticmethod
    def get_email_sender() -> str:
        return "default"

    @staticmethod
    def generate_table(rows, empty=" / "):
        """
        将行数据格式化成 html 的 table 格式
        :param rows: list
        :param empty: 单元格为空时的默认占位符
        :return: dominate.tags.table
        """
        table = dominate.tags.table()
        for row in rows:
            # 添加表头
            if len(table) == 0:
                tr = dominate.tags.tr()
                for field in row:
                    tr.add(dominate.tags.th(field))
                table.add(tr)
            tr = dominate.tags.tr()
            for field in row:
                value = row[field]
                if type(value) != str and ("占比" in field or field in ["同比", "环比"]):
                    value = str(Math.round(value * 100)) + "%"
                if empty != "" and (value == 0 or value == "" or value == '0.00%'):
                    tr.add(dominate.tags.td(empty, style="color: #999; font-size: 12px;"))
                else:
                    tr.add(dominate.tags.td(value))
            table.add(tr)
        return table

    @staticmethod
    def generate_table_style():
        """
        获取表格样式
        :return: dominate.tags.style
        """
        style = """
            html {
                font-family: Inter, 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
            }
            table {
                text-align: center;
                border: 1px solid #999;
                border-collapse:collapse;
            }
            table tr:first-child {
                background-color: #409eff;
            }
            table th {
                border: 1px solid #999;
                color: #fff;
                padding: 4px 10px;
            }
            table td {
                border: 1px solid #999;
                padding: 4px 10px;
            }
        """
        return dominate.tags.style(style)

    @staticmethod
    def generate_attachment_file_name(dir_name: str, ext_name="", prefix="attach") -> str:
        """
        生成随机附件名
        该方法不会生成文件，仅返回文件路径
        :param dir_name: 文件夹名称，存在于 runtime/attachments 目录下，不存在时将自动创建文件夹
        :param ext_name: 文件扩展名
        :param prefix: 文件前缀，默认是 attach ，可以手动指定
        :return:
        """
        path = f"runtime/attachments/{dir_name}"
        if not os.path.exists(path):
            os.mkdir(path)

        name = datetime.now().strftime("%Y%m%d%H%M%S")
        rand = str(random.randint(1000, 9999))
        result = f"{path}/{prefix}_{name}_{rand}"

        if ext_name != "":
            result = result + "." + ext_name
        return result
