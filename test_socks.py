import requests

proxy = '173.245.49.27:80'
protocols = ['http', 'https', 'socks4', 'socks5']
url = 'http://www.baidu.com'

for protocol in protocols:
    proxies = {
        'http': f'{protocol}://{proxy}',
        'https': f'{protocol}://{proxy}',
    }
    try:
        print(f"Testing with {protocol}...")
        response = requests.get(url, proxies=proxies, timeout=10)
        print(f"Status code: {response.status_code}")
        print(f"{protocol} is working!")
        break
    except Exception as e:
        print(e)