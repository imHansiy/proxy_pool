import requests

def test_proxy(max_retries=10):
    for i in range(max_retries):
        try:
            # 1. 从代理池获取一个代理IP
            print(f"\n--- 第 {i+1} 次尝试 ---")
            proxy_response = requests.get("http://localhost:5010/get")
            if proxy_response.status_code != 200:
                print(f"获取代理失败: {proxy_response.text}")
                continue

            proxy_ip = proxy_response.json().get("proxy")
            if not proxy_ip:
                print("代理池中无可用代理")
                break

            print(f"获取到代理IP: {proxy_ip}")

            # 2. 使用代理IP请求百度
            proxies = {
                "http": f"http://{proxy_ip}",
                "https": f"http://{proxy_ip}",
            }
            print("正在使用代理请求百度...")
            baidu_response = requests.get("https://www.baidu.com", proxies=proxies, timeout=10)

            # 3. 检查结果
            if baidu_response.status_code == 200:
                print("代理可用，成功访问百度！")
                return True
            else:
                print(f"代理不可用，访问百度失败，状态码: {baidu_response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
        except Exception as e:
            print(f"发生未知错误: {e}")

    print(f"\n尝试 {max_retries} 次后，仍未找到可用代理。")
    return False

if __name__ == "__main__":
    test_proxy()