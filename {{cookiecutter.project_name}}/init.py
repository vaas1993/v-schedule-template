import os

base = "init"


def parse_dir(path):
    files = os.listdir(path)
    for name in files:
        file = f"{path}/{name}"
        if os.path.isdir(file):
            parse_dir(file)
            continue
        absolute_file = file.replace(base + "/", "")

        if os.path.exists(absolute_file):
            print(f"文件 {absolute_file} 已存在")
            continue

        create = open(absolute_file, 'w')
        before = open(file, 'r')
        create.write(before.read())
        print(f"创建文件 {absolute_file}")


print("正在初始化项目...")
parse_dir(base)
print("初始化完成")
