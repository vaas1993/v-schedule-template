import threading
import mysql.connector.pooling

from config import main
from src.helpers.Logger import Logger

LOGGER = Logger()


class MySQL:
    # 用来实现单例
    _instance = None
    # 线程锁，用来实现单例
    _lock = threading.Lock()
    # 连接池
    pools = {}

    def __new__(cls, *args, **kwargs):
        """
        单例模式，调用者可以直接实例化类
        :param args:
        :param kwargs:
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_connect_pool()
        return cls._instance

    def _init_connect_pool(self):
        """
        实例化连接池
        :return:
        """
        for name in main.config["db"]:
            db_config = main.config["db"][name]
            self.pools[name] = mysql.connector.pooling.MySQLConnectionPool(
                pool_size=db_config["pool"],
                host=db_config["host"],
                port=db_config["port"],
                user=db_config["user"],
                password=db_config["password"],
                buffered=True
            )

    def get_connect(self, db: str) -> mysql.connector.pooling.PooledMySQLConnection:
        return self.pools[db].get_connection()

    def before(self, cursor, db_name: str):
        cursor.execute(f"use `{db_name}`;")

    def one(self, db_name: str, command: str, db="default") -> dict:
        """
        获取单条数据
        :param db_name: 数据库名称
        :param command: SQL语句
        :param db: 数据库
        :return: dict 或者 None
        """
        conn = self.get_connect(db)
        cursor = conn.cursor()
        self.before(cursor, db_name)
        cursor.execute(command)
        columns = [column[0] for column in cursor.description]
        row = cursor.fetchone()
        if row is not None:
            row = dict(zip(columns, row))
        cursor.close()
        conn.close()
        return row

    def batch(self, db_name: str, command: str, db="default") -> list:
        """
        批量查询
        :param db_name: 数据库名称
        :param command: SQL语句
        :param db: 数据库
        :return: list
        """
        conn = self.get_connect(db)
        cursor = conn.cursor()
        self.before(cursor, db_name)
        cursor.execute(command)
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        for index in range(len(rows)):
            rows[index] = dict(zip(columns, rows[index]))
        cursor.close()
        conn.close()
        return rows

    def execute(self, db_name: str, command: str, db="default") -> None:
        """
        仅执行SQL
        :param db_name: 数据库名称
        :param command: SQL语句
        :param db: 数据库
        :return: None
        """
        conn = self.get_connect(db)
        cursor = conn.cursor()
        self.before(cursor, db_name)
        cursor.execute(command)
        conn.commit()
        cursor.close()
        conn.close()

    def execute_many(self, db_name: str, command: str, data: list, db="default", ) -> None:
        """
        执行批量插入SQL
        :param data:
        :param db_name: 数据库名称
        :param command: SQL语句
        :param db: 数据库
        :return: None
        """
        conn = self.get_connect(db)
        cursor = conn.cursor()
        self.before(cursor, db_name)
        cursor.executemany(command, data)
        conn.commit()
        cursor.close()
        conn.close()
