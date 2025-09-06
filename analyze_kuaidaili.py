# -*- coding: utf-8 -*-
"""
分析 kuaidaili_page_1.html 文件，找出代理信息结构
"""

from bs4 import BeautifulSoup
import re

def analyze_kuaidaili_html(file_path):
    """分析快代理HTML文件"""
    print(f"正在分析文件: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    soup = BeautifulSoup(content, 'html.parser')
    
    # 1. 查找所有 table 元素及其子元素
    print("\n=== 查找所有 table 元素 ===")
    tables = soup.find_all('table')
    print(f"找到 {len(tables)} 个 table 元素")
    
    for i, table in enumerate(tables):
        print(f"\n--- Table {i+1} ---")
        print(f"Class: {table.get('class')}")
        print(f"ID: {table.get('id')}")
        
        # 查找 thead
        thead = table.find('thead')
        if thead:
            print("  找到 thead:")
            headers = thead.find_all('th')
            for j, th in enumerate(headers):
                print(f"    Header {j+1}: {th.text.strip()}")
        else:
            print("  未找到 thead")
            
        # 查找 tbody
        tbody = table.find('tbody')
        if tbody:
            print("  找到 tbody:")
            rows = tbody.find_all('tr')
            print(f"    找到 {len(rows)} 行数据")
            for k, tr in enumerate(rows[:3]): # 只打印前3行
                tds = tr.find_all('td')
                print(f"      Row {k+1}: {len(tds)} 列")
                for l, td in enumerate(tds):
                    print(f"        Col {l+1}: {td.text.strip()}")
        else:
            print("  未找到 tbody")
            
    # 2. 查找所有 class 包含 'table' 的元素
    print("\n=== 查找所有 class 包含 'table' 的元素 ===")
    table_like_elements = soup.find_all(class_=lambda x: x and 'table' in x.lower())
    print(f"找到 {len(table_like_elements)} 个 class 包含 'table' 的元素")
    
    for i, elem in enumerate(table_like_elements):
        print(f"\n--- Element {i+1} ---")
        print(f"Tag: {elem.name}")
        print(f"Class: {elem.get('class')}")
        print(f"ID: {elem.get('id')}")
        
        # 如果是 div 或其他容器，查找其子元素
        children = list(elem.children)
        if children:
            print(f"  子元素数量: {len(children)}")
            # 查找直接子元素中的 tr
            trs = elem.find_all('tr', recursive=False)
            if trs:
                print(f"  直接子元素中找到 {len(trs)} 个 tr")
                for k, tr in enumerate(trs[:3]):  # 只打印前3行
                    tds = tr.find_all('td')
                    print(f"    Row {k+1}: {len(tds)} 列")
                    for l, td in enumerate(tds):
                        print(f"      Col {l+1}: {td.text.strip()}")
            else:
                # 查找所有后代中的 tr
                all_trs = elem.find_all('tr')
                if all_trs:
                    print(f"  后代元素中找到 {len(all_trs)} 个 tr")
                    for k, tr in enumerate(all_trs[:3]):  # 只打印前3行
                        tds = tr.find_all('td')
                        print(f"    Row {k+1}: {len(tds)} 列")
                        for l, td in enumerate(tds):
                            print(f"      Col {l+1}: {td.text.strip()}")
                else:
                    print("  未找到 tr 元素")
        else:
            print("  没有子元素")
            
    # 3. 尝试通过文本内容查找 IP 和端口
    print("\n=== 通过文本内容查找 IP 和端口 ===")
    # 查找所有文本包含 IP 地址格式的内容
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    text_elements = soup.find_all(string=ip_pattern)
    print(f"找到 {len(text_elements)} 个包含 IP 地址的文本节点")
    
    # 查找包含端口的文本 (通常是 1-5 位数字)
    port_pattern = re.compile(r'\b[0-9]{1,5}\b')
    port_text_elements = soup.find_all(string=port_pattern)
    print(f"找到 {len(port_text_elements)} 个包含数字的文本节点 (可能是端口)")
    
    # 4. 查找所有 tr 元素，然后检查其父元素和兄弟元素
    print("\n=== 查找所有 tr 元素 ===")
    all_trs = soup.find_all('tr')
    print(f"找到 {len(all_trs)} 个 tr 元素")
    
    # 检查前几个 tr 元素
    for i, tr in enumerate(all_trs[:10]):
        tds = tr.find_all('td')
        if len(tds) >= 2:
            # 检查第一列和第二列是否可能是 IP 和端口
            ip_text = tds[0].text.strip()
            port_text = tds[1].text.strip()
            if ip_pattern.match(ip_text) and port_pattern.match(port_text):
                print(f"  可能的代理信息 (行 {i+1}): IP={ip_text}, Port={port_text}")
                # 打印更多列信息
                for j, td in enumerate(tds):
                    print(f"    Col {j+1}: {td.text.strip()}")
                print("  ---")
        else:
            print(f"  行 {i+1} 列数不足: {len(tds)}")

# 分析文件
analyze_kuaidaili_html('kuaidaili_page_1.html')