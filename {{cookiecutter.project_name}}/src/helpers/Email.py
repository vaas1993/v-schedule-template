import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.main import config

from src.helpers.Logger import Logger

LOGGER = Logger()

"""
邮件类，用来发送邮件
"""


class Email:
    def __init__(self):
        # 邮件标题
        self.subject = ""

        # 邮件接收地址，这是个字符串列表，每个元素都是一个接收又想
        self.receivers = []

        # 抄送列表，格式和接收地址一致
        self.ccs = []

        # 附件列表
        self.attachments = []

        # 邮件正文
        self.content = None

    def set_subject(self, subject: str):
        """
        设置邮件标题
        :param subject:
        :return:
        """
        self.subject = subject

    def set_content(self, content: str):
        """
        设置邮箱正文
        :param content: str
        :return:
        """
        self.content = content

    def set_receivers(self, receivers: list):
        """
        设置收件人列表
        :param receivers: str[]
        :return:
        """
        self.receivers = receivers

    def set_ccs(self, ccs: list):
        """
        设置抄送列表
        :param ccs: str[]
        :return:
        """
        self.ccs = ccs

    def add_attachment(self, path: str, name: str):
        """
        添加附件
        :param path: 附件路径
        :param name: 附件展示名
        :return:
        """
        self.attachments.append({
            "path": path,
            "name": name
        })

    def send(self, sender="default", timeout=30) -> bool:
        """
        发送邮件
        :param sender: 发送人，可在主配置文件 config/main.py 中的 mail 项查看
        :param timeout: 超时时间，秒
        :return:
        """

        mail = MIMEMultipart()

        # 获取发件人配置
        sender_config = config["mail"][sender]

        # 标题
        mail["Subject"] = self.subject
        # 发件人
        mail["From"] = sender_config["user"]
        # 收件人
        mail["To"] = ", ".join(self.receivers)
        # 抄送人
        mail["Cc"] = ", ".join(self.ccs)
        # 邮件正文
        mail.attach(MIMEText(self.content, "html"))

        # 附件
        for item in self.attachments:
            attachment = MIMEApplication(open(item["path"], 'rb').read())
            attachment['Content-Type'] = 'application/octet-stream'
            attachment.add_header('Content-Disposition', 'attachment', filename=('gbk', '', item["name"]))
            mail.attach(attachment)

        try:
            server = smtplib.SMTP_SSL(host=sender_config["server"], port=sender_config["port"], timeout=timeout)
            server.login(sender_config["user"], sender_config["password"])
            recipients = self.receivers
            if len(self.ccs) > 0:
                recipients += self.ccs
            server.sendmail(mail['From'], recipients, mail.as_string())
            LOGGER.success(f"邮件 {self.subject} 发送成功")
            return True
        except Exception as e:
            LOGGER.err(f"邮件 {self.subject} 发送失败：" + str(e))
        return False
