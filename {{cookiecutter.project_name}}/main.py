import _thread

from config.main import config
from src.helpers.Logger import Logger
from src.helpers.TaskManager import TaskManager

LOGGER = Logger()
LOGGER.log(config["welcome"])
LOGGER.log("正在加载任务配置...")

# 实例化任务管理器，并开启任务调度器
manager = TaskManager()
manager.start()

# 启动一个子线程，定期从数据库更新任务
_thread.start_new_thread(manager.listen, ())

try:
    manager.runner.listen()
except KeyboardInterrupt:
    LOGGER.log("程序退出")
