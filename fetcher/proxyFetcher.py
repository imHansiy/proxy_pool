
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
    def freeProxy06():
        """ 冰凌代理 https://www.binglx.cn """
        url = "https://www.binglx.cn/?page=1"
        try:
            tree = WebRequest().get(url).tree
            proxy_list = tree.xpath('.//table//tr')
            for tr in proxy_list[1:]:
                yield Proxy(':'.join(tr.xpath('./td/text()')[0:2]))
        except Exception as e:
            print(e)

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
    def freeProxy09(page_count=1):
        """ 免费代理库 """
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?country=中国&page={}'.format(i)
            html_tree = WebRequest().get(url, verify=False).tree
            for index, tr in enumerate(html_tree.xpath("//table//tr")):
                if index == 0:
                    continue
                yield Proxy(":".join(tr.xpath("./td/text()")[0:2]).strip())

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
        快代理 (通过解析内嵌JS数据获取) https://www.kuaidaili.com/free/intr/{page}/
        """
        # 遍历前三页
        for page in range(1, 4):
            url = f"https://www.kuaidaili.com/free/intr/{page}/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
            try:
                r = WebRequest().get(url, header=headers, timeout=10)
                if not r or not r.text:
                    continue  # 继续尝试下一页

                # 使用正则表达式提取 const fpsList = [...] 的内容
                match = re.search(r'const fpsList = (\[.*?\]);', r.text, re.DOTALL)
                if match:
                    json_str = match.group(1)
                    data_list = json.loads(json_str)

                    for item in data_list:
                        ip = item.get('ip')
                        port = item.get('port')
                        region = item.get('location', '')
                        anonymous = '高匿名'
                        protocol = 'http'

                        if ip and port:
                            proxy_str = f"{ip}:{port}"
                            yield Proxy(proxy=proxy_str, region=region, anonymous=anonymous, protocol=protocol, source="freeProxy12")
            except Exception as e:
                print(f"Failed to fetch from freeProxy12 page {page}: {e}")


if __name__ == '__main__':
    p = ProxyFetcher()
    for _ in p.freeProxy12():
        print(_)
