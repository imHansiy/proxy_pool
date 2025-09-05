.. _ext_fetcher:

扩展代理源
===========

项目默认包含几个免费的代理获取源，但免费代理质量有限。为了获取更稳定、高效的代理，本项目支持用户自定义扩展代理获取源。

核心原则
--------

*   **一个来源，一个函数**：每一个新的代理网站对应一个独立的采集函数。
*   **静态方法**：所有采集函数都必须是 ``ProxyFetcher`` 类的 ``@staticmethod``。
*   **生成器模式**：函数必须使用 ``yield`` 关键字返回 ``Proxy`` 对象，而不是一次性返回一个列表。这有利于内存管理。
*   **健壮性**：必须包含异常处理逻辑，以应对网络错误或目标网站结构变更。

实现步骤
--------

**第 1 步：创建采集函数**

1.  **文件位置**：打开 ``fetcher/proxyFetcher.py``。
2.  **函数命名**：在 ``ProxyFetcher`` 类中，创建一个新的静态方法。方法名应遵循 ``freeProxyXX`` 的格式，其中 ``XX`` 是一个唯一的数字编号。
3.  **函数文档**：为函数添加清晰的文档字符串（docstring），说明代理源的名称和网址。

**第 2 步：获取网页内容**

1.  **使用 WebRequest**：调用 ``util.webRequest.WebRequest`` 类来获取网页内容。
2.  **模拟浏览器**：强烈建议在请求时设置 ``User-Agent`` 请求头，以避免被简单的反爬虫机制拦截。

    .. code-block:: python

        from util.webRequest import WebRequest
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        r = WebRequest().get(url, header=headers)

**第 3 步：解析内容并提取数据**

1.  **解析工具**：
    *   对于 **HTML** 内容，使用 ``bs4.BeautifulSoup`` 进行解析。
    *   对于 **JSON** 内容，使用 ``json.loads(r.text)`` 进行解析。
2.  **提取字段**：从解析后的内容中，提取以下信息。**IP 和端口为必填项**，其他为选填项。
    *   ``ip`` (字符串)
    *   ``port`` (字符串)
    *   ``region`` (字符串): 代理的地理位置（国家/城市）。
    *   ``anonymous`` (字符串): 匿名程度（如：高匿、透明等）。
    *   ``protocol`` (字符串): 代理协议（如：http, https, socks5）。

**第 4 步：实例化并返回 Proxy 对象**

将提取出的信息作为参数，创建 ``Proxy`` 对象，并使用 ``yield`` 返回。务必设置 ``source`` 参数为当前函数名，用于溯源。

.. code-block:: python

    from helper.proxy import Proxy
    
    proxy_str = f"{ip}:{port}"
    yield Proxy(proxy=proxy_str, 
                region=region, 
                anonymous=anonymous, 
                protocol=protocol, 
                source="freeProxyXX")  # source 值必须与函数名一致

**第 5 步：添加异常处理**

将网络请求和解析代码包裹在 ``try...except`` 块中，捕获并打印异常。

**第 6 步：注册新函数**

在 ``ProxyFetcher`` 类的 ``__init__`` 方法中，将你新创建的函数（例如 ``self.freeProxyXX``）添加到 ``self.fetch_funcs`` 列表中。

.. code-block:: python

    def __init__(self, strategy="all"):
        self.__proxies__ = []
        self.fetch_funcs = [
            self.freeProxy06,
            # ...
            self.freeProxyXX  # <-- 在这里添加你的新函数
        ]

完整代码模板
------------

请复制以下模板，并根据目标网站的实际情况进行修改。

.. code-block:: python

    # 请将此函数模板添加到 fetcher/proxyFetcher.py 的 ProxyFetcher 类中

    @staticmethod
    def freeProxyXX():  # <-- 1. 更改函数名 (例如 freeProxy13)
        """
        <代理源名称和描述，例如：神奇代理 http://www.shenqi.com>
        """
        url_pattern = "<目标网站的URL格式>" # <-- 2. 填写URL
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        try:
            r = WebRequest().get(url_pattern, header=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # --- 3. 在下方编写你的核心解析逻辑 ---
            
            # 示例：解析HTML表格
            # for tr in soup.find('table').find_all('tr'):
            #     tds = tr.find_all('td')
            #     if len(tds) >= 5:
            #         ip = tds.text.strip()
            #         port = tds.text.strip()
            #         # ... 提取其他字段 ...
            #
            #         proxy_str = f"{ip}:{port}"
            #         yield Proxy(proxy=proxy_str, source="freeProxyXX") # <-- 4. source要和函数名一致
            
            # --- 解析逻辑结束 ---
            
        except Exception as e:
            print(f"Failed to fetch from freeProxyXX: {e}") # <-- 5. 异常处理中的函数名要一致

    # 最后，不要忘记在 ProxyFetcher 的 __init__ 方法中注册你的新函数！