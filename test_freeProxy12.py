# -*- coding: utf-8 -*-
"""
测试 freeProxy12 函数
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from util.webRequest import WebRequest
from bs4 import BeautifulSoup

def freeProxy12(page_count=1):
    """ 快代理 https://www.kuaidaili.com """
    url_pattern = "https://www.kuaidaili.com/free/intr/{}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    for i in range(1, page_count + 1):
        url = url_pattern.format(i)
        print(f"正在请求 URL: {url}")
        try:
            r = WebRequest().get(url, header=headers, timeout=10)
            if not r:
                print("请求返回空响应")
                continue
            
            # 通过 r.response 获取 requests.Response 对象
            status_code = r.response.status_code
            print(f"响应状态码: {status_code}")
            
            # 检查状态码
            if status_code != 200:
                print(f"请求失败，状态码: {status_code}")
                continue
                
            # 将完整的响应内容保存到文件
            with open(f'kuaidaili_page_{i}.html', 'w', encoding='utf-8') as f:
                f.write(r.text)
            print(f"已将页面内容保存到 kuaidaili_page_{i}.html")
            
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # 尝试找到包含代理信息的元素
            # 根据页面内容分析，代理信息可能在不同的元素中
            # 先尝试找 table
            table = soup.find('table')
            if table:
                print("找到 table 元素")
                tbody = table.find('tbody')
                if tbody:
                    rows = tbody.find_all('tr')
                    print(f"找到 {len(rows)} 行数据 (通过 table)")
                    for tr in rows:
                        tds = tr.find_all('td')
                        if len(tds) >= 7:
                            ip = tds[0].text.strip()
                            port = tds[1].text.strip()
                            anonymous = tds[2].text.strip()
                            protocol = tds[3].text.strip().lower()
                            region = tds[4].text.strip()
                            proxy = f"{ip}:{port}"
                            yield {
                                "proxy": proxy,
                                "anonymous": anonymous,
                                "protocol": protocol,
                                "region": region
                            }
                        else:
                            print(f"行数据列数不足: {len(tds)}")
                else:
                    print("未找到 tbody 元素")
            else:
                print("未找到 table 元素")
                # 尝试其他可能的选择器
                # 例如，查找所有 class 包含 'table' 的元素
                tables = soup.find_all(class_=lambda x: x and 'table' in x.lower())
                if tables:
                    print(f"找到 {len(tables)} 个 class 包含 'table' 的元素")
                    for table in tables:
                        tbody = table.find('tbody')
                        if tbody:
                            rows = tbody.find_all('tr')
                            print(f"在 class='{table.get('class')}' 的 table 中找到 {len(rows)} 行数据")
                            for tr in rows:
                                tds = tr.find_all('td')
                                if len(tds) >= 7:
                                    ip = tds[0].text.strip()
                                    port = tds[1].text.strip()
                                    anonymous = tds[2].text.strip()
                                    protocol = tds[3].text.strip().lower()
                                    region = tds[4].text.strip()
                                    proxy = f"{ip}:{port}"
                                    yield {
                                        "proxy": proxy,
                                        "anonymous": anonymous,
                                        "protocol": protocol,
                                        "region": region
                                    }
                                else:
                                    print(f"行数据列数不足: {len(tds)}")
                        else:
                            print(f"class='{table.get('class')}' 的 table 中未找到 tbody")
                else:
                    print("未找到 class 包含 'table' 的元素")
                    
                # 如果还是没找到，尝试查找其他可能的结构
                # 例如，查找所有 tr 元素，然后检查其父元素
                trs = soup.find_all('tr')
                if trs:
                    print(f"找到 {len(trs)} 个 tr 元素")
                    # 检查前几个 tr 元素，看是否包含代理信息
                    for tr in trs[:10]:  # 只检查前10个
                        tds = tr.find_all('td')
                        if len(tds) >= 7:
                            # 粗略判断是否可能是代理信息
                            ip_port = tds[0].text.strip() + ':' + tds[1].text.strip()
                            if '.' in ip_port and ':' in ip_port:  # 简单判断是否像 IP:Port
                                ip = tds[0].text.strip()
                                port = tds[1].text.strip()
                                anonymous = tds[2].text.strip() if len(tds) > 2 else ''
                                protocol = tds[3].text.strip().lower() if len(tds) > 3 else ''
                                region = tds[4].text.strip() if len(tds) > 4 else ''
                                proxy = f"{ip}:{port}"
                                yield {
                                    "proxy": proxy,
                                    "anonymous": anonymous,
                                    "protocol": protocol,
                                    "region": region
                                }
                        else:
                            print(f"tr 元素列数不足: {len(tds)}")
                    
        except Exception as e:
            print(f"请求 {url} 时发生异常: {e}")

if __name__ == '__main__':
    print("开始测试 freeProxy12...")
    count = 0
    try:
        for proxy_info in freeProxy12():
            print(proxy_info)
            count += 1
            if count >= 5:  # 只打印前5个代理
                break
    except Exception as e:
        print(f"测试过程中发生异常: {e}")
    
    if count == 0:
        print("未获取到任何代理。")
    else:
        print(f"成功获取到 {count} 个代理。")
        
    print("测试完成。")