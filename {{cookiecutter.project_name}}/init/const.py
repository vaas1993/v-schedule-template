"""
程序运行时用到的一些常量在这里定义
由于 python 没有用于定义常量语法糖，所以我们约定这个文件下的变量均为常量
运行阶段保持只读访问，不要尝试修改它们，否则可能会引发重大缺陷
"""

# 环境，取值范围有 production / preview / test / development
ENV = "development"

# 当前是否生成环境
ENV_PRODUCTION = ENV == "production"

# 当前是否预发布环境
ENV_PREVIEW = ENV == "preview"

# 当前是否测试环境
ENV_TEST = ENV == "test"

# 当前是否开发环境
ENV_DEVELOPMENT = ENV == "development"

# 是否启用 DEBUG 模式，启动 DEBUG 模式后运行时会产生一些额外的数据（比如打印错误信息）
# 开启后会影响运行性能，生产环境建议关闭
DEBUG = True
