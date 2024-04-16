import const
from config import main
from src.dbs.MySQL import MySQL
from src.helpers.Logger import Logger
from src.loaders.BaseLoader import BaseLoader

"""
任务加载器
从数据库中 加载/更新 任务配置
"""

LOGGER = Logger()


class TaskLoader(BaseLoader):
    def run(self, first=False):
        # 从环境参数里获取仅加载的任务ID
        sub_command = ""
        try:
            ids = const.TASK_ID_LIST
            if type(ids) == list and len(ids) > 0:
                ids = ','.join([str(id) for id in ids])
                if first:
                    LOGGER.info(message=f"仅加载部分任务 # {ids}")
                sub_command = f"AND id IN ({ids})"
        except AttributeError:
            pass
        mysql = MySQL()
        command = f"SELECT id, `name`, `path`, params, `trigger`, update_time FROM task WHERE active = 1 {sub_command};"
        return mysql.batch(db_name=main.config["db_names"]["project"], command=command)
