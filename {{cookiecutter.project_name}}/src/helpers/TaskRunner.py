import concurrent.futures
import json
import threading

from config import main
from src.helpers.Logger import Logger

LOGGER = Logger()

"""
任务执行器
APSchedule 无论是线程池、进程池还是协程模式都可能因为忙碌而错过任务的执行
它的解决方案是设定震荡参数和误差参数，但在某些情况下还是可能存在漏任务的问题

这个类的目的就是解决漏任务的问题
这里还是采用线程池来执行任务，但添加任务执行的时候会先入队列，然后由一个阻塞方法来监听任务队列
当队列为空时监听方法会永久阻塞，直到有新任务添加唤醒监听方法
这样即能充分利用线程池带来的执行效率，也能有效避免因个别任务执行占用而错过任务的执行
"""


class TaskRunner:
    def __init__(self):
        self.jobs = []

        # 线程池，用来执行排队中的任务
        self.workers = concurrent.futures.ThreadPoolExecutor(max_workers=main.config["task"]["pool"])

        self.event = threading.Event()

    def add_jog(self, task: dict, class_name: str):
        """
        添加任务
        任务会被添加到任务队列，由线程池依次执行（先进先出）
        :param task: dict
        :param class_name: str
        :return:
        """
        self.jobs.append({
            "task": task,
            "class_name": class_name
        })

        if not self.event.is_set():
            self.event.set()

    def _pop(self):
        """
        取出一个任务，任务不存在时返回 None
        :return:
        """
        if self._has_job() == 0:
            return None
        return self.jobs.pop()

    def _has_job(self):
        return len(self.jobs) > 0

    def listen(self):
        """
        使任务队列进入监听状态，会阻塞运行
        :return:
        """

        while True:
            if not self._has_job():
                self.event.clear()
                self.event.wait()
            while True:
                item = self._pop()
                if item is None:
                    break
                self.workers.submit(run, item["task"], item["class_name"])


def run(task: dict, class_name):
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
        instance.runnable()
        LOGGER.success(f"任务 {task['name']} # {task['id']} 运行完成")
    except Exception as e:
        LOGGER.err(f"任务 {task['name']} # {task['id']} 运行出错 : ({e.__class__.__name__}) {str(e)}")
