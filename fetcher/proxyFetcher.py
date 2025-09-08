
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
            self.freeProxy11,
            self.freeProxy12,
            self.freeProxy13,
        ]

    @staticmethod
    def freeProxy11():
        """ 稻壳代理 https://www.docip.net/ """
        r = WebRequest().get("https://www.docip.net/data/free.json", timeout=10)
        try:
            for each in r.json['data']:
                yield Proxy(each['ip'])
        except Exception as e:
            print(f"Error fetching from docip.net: {e}. Response text: {r.text[:200]}") # 打印更多错误信息

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

    @staticmethod
    def freeProxy13():
        """
        ProxyMist 代理 https://proxymist.com/zh/protocols/
        """
        urls = [
            "https://proxymist.com/zh/protocols/socks5/",
            "https://proxymist.com/zh/protocols/socks4/",
            "https://proxymist.com/zh/protocols/http/"
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        for url in urls:
            try:
                r = WebRequest().get(url, header=headers, timeout=10)
                soup = BeautifulSoup(r.text, 'html.parser')
                table = soup.find('table', attrs={'id': 'proxylister-table'})
                if not table:
                    print(f"未在 {url} 中找到代理表格。")
                    continue

                for tr in table.find('tbody').find_all('tr'):
                    tds = tr.find_all('td')
                    if len(tds) >= 5:
                        ip = tds[0].text.strip()
                        port = tds[1].text.strip()
                        protocol_raw = tds[2].text.strip().lower()
                        # 将全角逗号和中文顿号替换为半角逗号，然后分割，只取第一个协议
                        protocol_raw = protocol_raw.replace('，', ',').replace('、', ',')
                        if ',' in protocol_raw:
                            protocol = protocol_raw.split(',')[0].strip()
                        else:
                            protocol = protocol_raw
                        
                        # 确保协议是 'http', 'https', 'socks4', 'socks5' 中的一种
                        if 'http' in protocol:
                            protocol = 'http'
                        elif 'https' in protocol:
                            protocol = 'https'
                        elif 'socks4' in protocol:
                            protocol = 'socks4'
                        elif 'socks5' in protocol:
                            protocol = 'socks5'
                        else:
                            protocol = 'http' # 默认设置为http
                        
                        anonymous = tds[3].text.strip()
                        region_div = tds[4].find('div', class_='px-2')
                        region = region_div.find('strong').text.strip() + ' ' + region_div.find_all('br')[-1].next_sibling.strip() if region_div and region_div.find('strong') else ''

                        proxy_str = f"{ip}:{port}"
                        yield Proxy(proxy=proxy_str, region=region, anonymous=anonymous, protocol=protocol, source="freeProxy13")
            except Exception as e:
                print(f"Failed to fetch from {url}: {e}")
            finally:
                sleep(1)


if __name__ == '__main__':
    p = ProxyFetcher()
    for _ in p.freeProxy12():
        print(_)
