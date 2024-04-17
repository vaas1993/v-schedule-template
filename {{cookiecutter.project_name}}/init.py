import os

# 初始化文件目录
base = "environment"

# 环境配置
envs = [
    {
        "name": "开发环境",
        "params": {
            "INIT_ENV": "development",
            "INIT_DEBUG": "True"
        }
    },
    {
        "name": "测试环境",
        "params": {
            "INIT_ENV": "test",
            "INIT_DEBUG": "True"
        }
    },
    {
        "name": "预发布环境",
        "params": {
            "INIT_ENV": "preview",
            "INIT_DEBUG": "False"
        }
    },
    {
        "name": "生产环境",
        "params": {
            "INIT_ENV": "production",
            "INIT_DEBUG": "False"
        }
    },
]
env = None


def parse_dir(path: str):
    files = os.listdir(path)
    for name in files:
        file = f"{path}/{name}"
        if os.path.isdir(file):
            parse_dir(file)
            continue
        absolute_file = file.replace(base + "/", "")

        if os.path.exists(absolute_file):
            print(f"文件 {absolute_file} 已存在，是否覆盖？")
            cover = input(f"请输入 yes, y, no 或者 n，默认 no: ").lower()
            if cover not in ['yes', 'y']:
                continue

        create = open(absolute_file, 'w')
        before = open(file, 'r')
        content = before.read()
        for key in env["params"]:
            content = content.replace("{{"+key+"}}", env["params"][key])
        create.write(content)
        print(f"创建文件 {absolute_file}")


print("请选择你希望初始化的环境")

for idx in range(len(envs)):
    print(f"[{idx}] {envs[idx]['name']}")

try:
    index = input("输入 [0-3进行选择，或输入 \"q\" 退出]: ")
    if index == 'q':
        raise KeyboardInterrupt
    env = envs[int(index)]
except KeyboardInterrupt:
    print("已退出")
    exit()

print(f"已选择{env['name']}")

parse_dir(base)

print("初始化完成")
