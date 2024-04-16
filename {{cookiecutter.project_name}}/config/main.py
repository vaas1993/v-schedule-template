"""
主配置文件
"""
import os

import config.dbs
import config.mails

config = {
    # 欢迎语
    "welcome": "欢迎使用任务调度系统",

    # 任务模块配置
    "task": {
        # 任务更新间隔，秒
        "duration": 60,
        # 设置一个 int 列表程序将只加载这部分任务，这在开发阶段很有用，设置为空列表、None、不定义时将自动忽略
        "range": [],
        # 任务执行器线程池数量
        "pool": max(4, os.cpu_count())
    },

    # 邮件配置
    "mail": {
        # 默认发件人
        "default": config.mails.EMAIL_163,
        # 网易企业邮箱
        "wangyi": config.mails.EMAIL_163,
    },

    # 数据库配置
    "db": {
        # 默认数据库
        "default": config.dbs.DB_MYSQL,
    },

    # 常用数据库名称
    "db_names": config.dbs.NAMES,

    # 开放配置，其它平台的接口请求在这里配置，然后在 open 模块中使用
    "open_config": {
    }
}
