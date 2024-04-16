import asyncio
import importlib
import json
import threading
from time import sleep
from config import main
from src.helpers.Logger import Logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler as Scheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from src.loaders.TaskLoader import TaskLoader

"""
任务管理器
1. 加载 / 更新任务列表
2. 监听并触发任务
"""

LOGGER = Logger()

# 注册协程池
LOOPS = [
    asyncio.new_event_loop(),
    asyncio.new_event_loop(),
    asyncio.new_event_loop(),
    asyncio.new_event_loop(),
]


async def run_task(task: dict, class_name):
    """
    监听任务触发的方法
    :param task: dict 任务数据
    :param class_name: 任务绑定的响应类
    :return:
    """
    instance = class_name()
    instance.set_params(json.loads(task["params"]))
    LOGGER.info(f"开始运行 {task['name']} # {task['id']} 任务")
    try:
        await instance.runnable()
        LOGGER.success(f"任务 {task['name']} # {task['id']} 运行完成")
    except Exception as e:
        LOGGER.err(f"任务 {task['name']} # {task['id']} 运行出错 : ({e.__class__.__name__}) {str(e)}")


def run(task: dict, class_name):
    """
    将任务运行在协程中
    :param task: dict 任务数据
    :param class_name: 任务绑定的响应类
    :return:
    """
    for loop in LOOPS:
        if not loop.is_running():
            asyncio.set_event_loop(loop)
            thread = threading.Thread(target=loop.run_until_complete, args=(run_task(task, class_name),))
            thread.start()
            thread.join()
            break


class TaskManager:
    def __init__(self):
        # 托管中的任务
        self.tasks = {}
        # 加载次数
        self.count = 0
        # 任务调度器
        self.scheduler = Scheduler()

    def start(self):
        """
        开启任务调度监听
        :return:
        """
        self.scheduler.start()

    def set_tasks(self, tasks: list):
        """
        设置最新的任务列表
        :param tasks: list
        :return:
        """
        newest = {}
        ids = []
        for task in tasks:
            ids.append(task["id"])
            # 添加新任务
            if task["id"] not in self.tasks:
                if self.add_task(task, "添加"):
                    newest[task['id']] = task
            # 更新任务
            else:
                if task["update_time"] != self.tasks[task["id"]]["update_time"]:
                    self.scheduler.remove_job(job_id=str(task["id"]))
                    if self.add_task(task, "更新"):
                        newest[task['id']] = task
                else:
                    newest[task['id']] = task
        # 删除不存在的任务
        for _id in self.tasks:
            if _id not in ids:
                task = self.tasks[_id]
                LOGGER.warn(f"移除任务 {task['name']} # {_id}")
                self.scheduler.remove_job(job_id=str(_id))
        self.tasks = newest

    def add_task(self, task: dict, mode: str) -> bool:
        """
        添加任务
        :param task: dict 任务体
        :param mode: 操作模式，用来修改日志打印的信息，添加 / 更新
        :return:
        """
        timer = self.get_timer(task)
        if timer is None:
            LOGGER.err(f"任务 {task['name']} # {task['id']} 触发器存在语法错误")
            return False
        if self.get_task_class(task['path']) is None:
            LOGGER.err(f"任务 {task['name']} # {task['id']} 配置的任务类 {task['path']} 不存在")
            return False

        LOGGER.log(f"{mode}任务 {task['name']} # {task['id']} : {task['trigger']}")

        self.scheduler.add_job(
            id=str(task["id"]),
            name=task['name'],
            args=[task, self.get_task_class(task["path"])],
            func=run,
            trigger=timer
        )
        return True

    @staticmethod
    def get_timer(task: dict):
        """
        实例化任务配置的触发器
        当配置有问题时返回 None
        :param task: dict 任务体
        :return:
        """
        if type(task['trigger']) == str:
            task['trigger'] = json.loads(task['trigger'])
        if "type" not in task["trigger"]:
            return None
        # 定时模式
        if task["trigger"]["type"].upper() == "CRON":
            return CronTrigger(**task["trigger"]["options"])
        # 间隔模式
        if task["trigger"]["type"].upper() == "INTERVAL":
            return IntervalTrigger(**task["trigger"]["options"])
        return None

    @staticmethod
    def get_task_class(path):
        """
        获取任务类
        :param path: string
        :return:
        """
        try:
            module = path.split(".").pop()
            return getattr(importlib.import_module(f"src.tasks.{path}"), module)
        except ModuleNotFoundError:
            pass
        return None

    def load_task(self):
        """
        加载一次任务
        :return:
        """
        self.set_tasks(TaskLoader().run(first=self.count == 0))
        self.count += 1

    def listen(self):
        """
        监听任务变化定期加载
        :return:
        """
        # 监听间隔
        duration = main.config["task"]["duration"]
        while True:
            self.load_task()
            sleep(duration)
