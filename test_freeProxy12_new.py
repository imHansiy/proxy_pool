from fetcher.proxyFetcher import ProxyFetcher
import sys
import os
import requests
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

def test_proxy_with_time(proxy_obj):
    try:
        proxy_str = f"http://{proxy_obj.proxy}"
        start_time = time.time()
        response = requests.get('http://httpbin.org/ip', proxies={'http': proxy_str, 'https': proxy_str}, timeout=5)
        end_time = time.time()

        if response.status_code == 200:
            print(f"代理可用: {proxy_obj.proxy} -> {response.json().get('origin')}，响应时间: {end_time - start_time:.2f}秒")
            return True
        else:
            print(f"代理不可用: {proxy_obj.proxy} (状态码: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"代理不可用: {proxy_obj.proxy} -> {e}")
        return False

print("开始测试 freeProxy12 并验证代理可用性（使用 httpbin.org/ip）...")
available_proxies_count = 0
try:
    for proxy_obj in ProxyFetcher.freeProxy12():
        if test_proxy_with_time(proxy_obj):
            available_proxies_count += 1
except Exception as e:
    print(f"测试过程中发生异常: {e}")

print(f"测试结束。共获取到 {available_proxies_count} 个可用代理。")