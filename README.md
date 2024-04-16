# 说明

> 这是一个基于 `APScheduler` 的任务调度程序，使用 `MySQL` 做任务存储以及和定时同步的线程，适合做中等数量的任务调度

# 初始化

> 使用 `cookiecutter` 进行工程初始化，如果你还没有安装请先安装它：

```shell
# MAC
brew install cookiecutter
# Debian
apt install cookiecutter
# pip
pip3 install cookiecutter
```

> 注意：使用 `pip` 安装时可能不会创建终端命令，你需要到公共库的 `bin` 目录找到 `cookiecutter` 命令

> 关于 `cookiecutter` 的其它安装和使用细节可前往 [这里](https://cookiecutter.readthedocs.io/en/stable/) 查看

> 有了 `cookiecutter` 后，我们可以很容易的初始化工程目录：

```shell
cookiecutter gh:vshen/v-schedule-template
```