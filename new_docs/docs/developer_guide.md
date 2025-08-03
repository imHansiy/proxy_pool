# 开发者指南

Proxy Pool 设计为可扩展的架构，允许开发者轻松添加自己的代理源和校验逻辑。本指南将介绍项目的核心模块以及如何进行扩展。

## 项目结构简介

-   **`fetcher/proxyFetcher.py`**: 定义了所有代理抓取器。每个抓取器都是 `ProxyFetcher` 类的一个静态方法。
-   **`helper/validator.py`**: 定义了代理校验逻辑。通过装饰器将函数注册为不同阶段的校验器。
-   **`handler/proxyHandler.py`**: 封装了对数据库中代理的增、删、改、查等核心操作。
-   **`db/`**: 数据库客户端模块，实现了对 Redis 和 SSDB 的支持。
-   **`api/proxyApi.py`**: 提供了对外服务的 HTTP API 接口。
-   **`proxyPool.py`**: 项目的命令行启动入口和调度器主逻辑。

## 如何扩展代理源

项目默认包含了一些免费的代理源，但它们的质量可能不稳定。你可以通过以下步骤添加自己的代理获取渠道（例如，付费代理 API、自己搭建的代理服务器等）。

**1. 添加抓取方法**

打开 `fetcher/proxyFetcher.py` 文件，在 `ProxyFetcher` 类中添加一个新的静态方法。这个方法必须：
-   是一个生成器 (使用 `yield`)。
-   返回 `ip:port` 格式的字符串。

**示例：**

```python
# In fetcher/proxyFetcher.py
class ProxyFetcher(object):
    # ... existing methods

    @staticmethod
    def myCustomProxySource():
        """
        一个自定义的代理源。
        可以从网站、API 或数据库获取代理。
        """
        # 假设你从某个 API 获取了代理列表
        proxies_from_api = ["10.0.0.1:8888", "10.0.0.2:8888"]
        for proxy in proxies_from_api:
            # 确保返回格式正确
            yield proxy
```

**2. 启用新的抓取器**

打开根目录下的 `setting.py` 文件，将你刚刚创建的方法名添加到 `PROXY_FETCHER` 列表中。

```python
# In setting.py
PROXY_FETCHER = [
    "freeProxy01",
    # ... other fetchers
    "myCustomProxySource"  # 添加你的自定义方法名
]
```

完成以上两步后，重启调度器，它就会自动调用你的新方法来获取代理了。

## 如何扩展代理校验逻辑

代理校验分为三个阶段，通过装饰器来区分：

-   `@ProxyValidator.preValidator`: **预校验**。在代理入库前进行，通常用于检查代理格式是否正确。
-   `@ProxyValidator.httpValidator`: **HTTP 可用性校验**。检查代理是否能正常访问 HTTP 网站。只有通过此阶段所有校验的代理才会被认为是可用代理。
-   `@ProxyValidator.httpsValidator`: **HTTPS 可用性校验**。检查通过了 HTTP 校验的代理是否也支持 HTTPS。

当一个阶段有多个校验函数时，它们会按定义顺序执行，**必须所有函数都返回 `True`**，该阶段的校验才算通过。

**示例：添加一个自定义的 HTTP 校验器**

假设你需要确保代理不仅能访问目标网站，还能获取到特定的关键词，可以添加如下校验函数。

1.  打开 `helper/validator.py` 文件。
2.  添加你的自定义校验函数，并使用相应的装饰器。

```python
# In helper/validator.py
fromrequests.compatimport chardet

# ...

@ProxyValidator.addHttpValidator
def customKeywordValidator(proxy):
    """
    自定义校验器：检查代理访问百度首页是否能返回特定关键词。
    """
    proxies = {"http": f"http://{proxy.proxy}"}
    try:
        # 使用 verify=False 是因为我们只关心内容，不校验证书
        r = requests.get("http://www.baidu.com", headers=HEADER, proxies=proxies, timeout=5, verify=False)
        # 检测编码并解码
        encoding = chardet.detect(r.content)['encoding']
        content = r.content.decode(encoding or 'utf-8')

        if r.status_code == 200 and "百度一下" in content:
            return True
        return False
    except Exception:
        return False
```

添加后，这个 `customKeywordValidator` 会自动被加入到 HTTP 校验流程中。你无需修改其他任何配置。同理，你也可以使用 `@ProxyValidator.addHttpsValidator` 来添加自定义的 HTTPS 校验逻辑。