import requests
import sys

# The SOCKS proxy to be tested.
# You can change this to the proxy you want to test.
proxy_address = '173.245.49.27:80'

# If a proxy address is provided as a command-line argument, use it.
if len(sys.argv) > 1:
    proxy_address = sys.argv[1]

# Protocols to test. We prioritize SOCKS protocols.
protocols = ['socks5', 'socks4', 'http', 'https']

# A reliable URL for testing connectivity.
test_url = 'http://www.baidu.com'

print(f"--- Starting Proxy Test for: {proxy_address} ---")
print(f"--- Testing against URL: {test_url} ---")
print("-" * 40)

is_working = False

for protocol in protocols:
    proxies = {
        'http': f'{protocol}://{proxy_address}',
        'https': f'{protocol}://{proxy_address}',
    }
    try:
        print(f"[*] Testing protocol: {protocol}...")
        # Set a timeout to avoid waiting indefinitely.
        response = requests.get(test_url, proxies=proxies, timeout=10)

        if response.status_code == 200:
            print(f"[+] SUCCESS!")
            print(f"    - Protocol '{protocol}' is working.")
            print(f"    - Status Code: {response.status_code}")
            is_working = True
            break  # Stop testing after finding a working protocol
        else:
            print(f"[-] FAILED: Received a non-200 status code: {response.status_code}")

    except requests.exceptions.ProxyError as e:
        print(f"[-] FAILED: Cannot connect to proxy.")
        print(f"    - Detail: This often means the proxy is offline or the protocol '{protocol}' is incorrect.")
    except requests.exceptions.ConnectTimeout:
        print(f"[-] FAILED: Connection timed out.")
        print(f"    - Detail: The proxy is too slow or unreachable.")
    except Exception as e:
        print(f"[-] FAILED: An unexpected error occurred.")
        print(f"    - Detail: {e}")
    finally:
        print("-" * 40)

if is_working:
    print(f"--- Test Result: Proxy {proxy_address} is WORKING. ---")
else:
    print(f"--- Test Result: Proxy {proxy_address} is NOT WORKING with tested protocols. ---")
