# 快速上手

本指南将引导你完成 Proxy Pool 项目的下载、安装、配置和启动。

## 1. 下载代码

首先，你需要将项目代码克隆到本地。打开你的终端，使用 `git` 命令：

```bash
git clone https://github.com/jhao104/proxy_pool.git
```

如果你不需要完整的提交历史，也可以从 [GitHub Releases](https://github.com/jhao104/proxy_pool/releases) 页面下载最新的稳定版本压缩包。

## 2. 安装依赖

进入项目根目录，使用 `pip` 安装所需的依赖库。

```bash
cd proxy_pool
pip install -r requirements.txt
```

确保你的 Python 环境是 3.6 或更高版本。

## 3. 修改配置

项目的核心配置位于根目录下的 `setting.py` 文件中。你可以根据自己的需求修改以下关键配置：

```python
# API 服务配置
HOST = "0.0.0.0"  # 监听的 IP 地址，0.0.0.0 表示允许所有 IP 访问
PORT = 5010        # 监听的端口号

# 数据库配置 (支持 Redis 和 SSDB)
# 示例:
#   - Redis: redis://:password@ip:port/db
#   - Ssdb:  ssdb://:password@ip:port
DB_CONN = 'redis://@127.0.0.1:6379/0'

# 启用的代理抓取器
# 所有可用的抓取器都定义在 fetcher/proxyFetcher.py 文件中
PROXY_FETCHER = [
    "freeProxy01",
    "freeProxy02",
    # ... 你可以在此添加或移除抓取器
]
```

更详细的配置说明，请参考 [配置详解](configuration.md) 页面。

## 4. 启动项目

项目由两部分组成：

*   **调度器 (`schedule`)**: 负责从各大代理源网站抓取、校验和存储代理。
*   **Web 服务 (`server`)**: 提供 HTTP API 接口，供外部程序获取代理。

你需要分别启动这两个组件。

**启动调度器：**

在终端中运行以下命令，启动代理的抓取和校验任务。

```bash
python proxyPool.py schedule
```

**启动 API 服务：**

打开一个新的终端窗口，运行以下命令，启动 Web API 服务。

```bash
python proxyPool.py server
```

服务启动后，你可以通过访问 `http://127.0.0.1:5010` 来查看 API 的基本信息和使用说明。