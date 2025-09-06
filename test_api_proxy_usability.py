import requests
import time
import sys
import os

# 将项目根目录添加到 sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

def get_proxy_from_api(proxy_type=''):
    """从本地API获取一个代理，可指定类型（http/https）"""
    api_url = f'http://proxy_pool:5010/get/?type={proxy_type}'
    max_retries = 5  # 最多尝试获取5次
    for i in range(max_retries):
        try:
            print(f"尝试从API获取代理 (第 {i+1}/{max_retries} 次), 类型: {proxy_type if proxy_type else 'any'}...")
            response = requests.get(api_url, timeout=15) # 增加获取API代理的超时时间
            response.raise_for_status()  # 检查HTTP错误
            proxy_data = response.json()
            if proxy_data and proxy_data.get('proxy'):
                print(f"成功从API获取代理: {proxy_data['proxy']}")
                return proxy_data['proxy']
            else:
                print("API未返回可用代理，尝试重新获取。")
        except requests.exceptions.RequestException as e:
            print(f"从API获取代理失败: {e}，尝试重新获取。")
        time.sleep(1) # 等待1秒后重试
    print("未能从API获取到可用代理，达到最大重试次数。")
    return None

def test_proxy_with_time(proxy_str):
    """测试代理是否能请求HTTPS网站（例如Bing），并获取响应时间"""
    test_url = 'https://www.bing.com'
    try:
        start_time = time.time()
        proxies = {
            'http': f"http://{proxy_str}",
            'https': f"http://{proxy_str}"
        }
        print(f"正在使用代理设置: {proxies} 访问 {test_url}")
        response = requests.get(test_url, proxies=proxies, timeout=15) # 增加访问目标网站的超时时间
        end_time = time.time()

        response.raise_for_status() # 检查HTTP错误
        
        if response.status_code == 200:
            print(f"代理可用: {proxy_str} -> 成功请求 {test_url}，响应时间: {end_time - start_time:.2f}秒")
            return True
        else:
            print(f"代理不可用: {proxy_str} -> 请求 {test_url} 失败，状态码: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"代理不可用: {proxy_str} -> 请求 {test_url} 异常: {e}")
        return False

if __name__ == "__main__":
    print("开始测试从API获取的代理可用性...")
    # 尝试获取HTTPS代理
    retrieved_proxy = get_proxy_from_api(proxy_type='https')

    if retrieved_proxy:
        if test_proxy_with_time(retrieved_proxy):
            print("代理验证成功！")
        else:
            print("代理验证失败。")
    else:
        print("未能从API获取到代理，无法进行可用性测试。")

    print("测试结束。")
