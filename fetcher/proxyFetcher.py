
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxyFetcher
   Description :
   Author :        JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
-------------------------------------------------
"""
__author__ = 'JHao'

import re
import json
import sys
import os
from time import sleep
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.webRequest import WebRequest
from helper.proxy import Proxy


class ProxyFetcher(object):
    """
    proxy getter
    """

    def __init__(self, strategy="all"):
        self.__proxies__ = []
        self.fetch_funcs = [
            self.freeProxy12,
        ]

    @staticmethod
    def freeProxy07():
        """ 云代理 """
        urls = ['http://www.ip3366.net/free/?stype=1', "http://www.ip3366.net/free/?stype=2"]
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield Proxy(":".join(proxy))

    @staticmethod
    def freeProxy10():
        """ 89免费代理 """
        r = WebRequest().get("https://www.89ip.cn/index_1.html", timeout=10)
        proxies = re.findall(
            r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
            r.text)
        for proxy in proxies:
            yield Proxy(':'.join(proxy))

    @staticmethod
    def freeProxy11():
        """ 稻壳代理 https://www.docip.net/ """
        r = WebRequest().get("https://www.docip.net/data/free.json", timeout=10)
        try:
            for each in r.json['data']:
                yield Proxy(each['ip'])
        except Exception as e:
            print(e)


    @staticmethod
    def freeProxy12():
        """
        快代理 (通过解析内嵌JS数据获取)
        同时抓取国内代理 (https://www.kuaidaili.com/free/intr/{page}/)
        和海外免费代理 (https://www.kuaidaili.com/free/fps/{page}/)
        """
        url_patterns = [
            "https://www.kuaidaili.com/free/intr/{}/",  # 国内免费代理
            "https://www.kuaidaili.com/free/fps/{}/"    # 海外免费代理
        ]

        # 遍历前三页和两种URL模式
        for url_pattern in url_patterns:
            for page in range(1, 4):
                url = url_pattern.format(page)
                try:
                    headers_fps = {
                        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
                        'Accept': '*/*',
                        'Host': 'www.kuaidaili.com',
                        'Connection': 'keep-alive',
                        'Cookie': 'channelid=0; sid=1757151338733991'
                    }
                    if "intr" in url:
                        r = WebRequest().get(url, timeout=15, retry_time=1) # intr 页面继续使用默认headers
                    else: # fps 页面使用提供的headers
                        r = WebRequest().get(url, header=headers_fps, timeout=15, retry_time=1)
                    if not r or not r.text:
                        print(f"Failed to get content from {url}")
                        sleep(2) # 增加延时，防止被反爬
                        continue  # 继续尝试下一页或下一个模式

                    if "intr" in url: # 国内代理仍然使用fpsList解析
                        print(f"--- Content from {url} (first 500 chars) ---")
                        print(r.text[:500])
                        print(f"--- End Content from {url} ---")
                        match = re.search(r'const fpsList = (\[.*?\]);', r.text, re.DOTALL)
                        if match:
                            json_str = match.group(1)
                            data_list = json.loads(json_str)
                            print(f"成功从 {url} 获取到 {len(data_list)} 个代理。") # 打印获取数量
                            for item in data_list:
                                ip = item.get('ip')
                                port = item.get('port')
                                region = item.get('location', '')
                                anonymous = '高匿名'
                                protocol = 'http'
                                if ip and port:
                                    proxy_str = f"{ip}:{port}"
                                    yield Proxy(proxy=proxy_str, region=region, anonymous=anonymous, protocol=protocol, source="freeProxy12")
                        else:
                            print(f"未能在 {url} 中找到 'const fpsList' 结构。")
                    elif "fps" in url: # 海外代理也尝试使用fpsList解析
                        print(f"--- Content from {url} (first 500 chars) ---")
                        print(r.text[:500])
                        print(f"--- End Content from {url} ---")
                        match = re.search(r'const fpsList = (\[.*?\]);', r.text, re.DOTALL)
                        if match:
                            json_str = match.group(1)
                            data_list = json.loads(json_str)
                            print(f"成功从 {url} 获取到 {len(data_list)} 个代理。")
                            for item in data_list:
                                ip = item.get('ip')
                                port = item.get('port')
                                region = item.get('location', '')
                                anonymous = '高匿名'
                                protocol = 'http'
                                if ip and port:
                                    proxy_str = f"{ip}:{port}"
                                    yield Proxy(proxy=proxy_str, region=region, anonymous=anonymous, protocol=protocol, source="freeProxy12")
                        else:
                            print(f"未能在 {url} 中找到 'const fpsList' 结构。")
                except Exception as e:
                    print(f"Failed to fetch from {url}: {e}")
                finally:
                    sleep(1) # 增加延时，防止被反爬


if __name__ == '__main__':
    p = ProxyFetcher()
    for _ in p.freeProxy12():
        print(_)
