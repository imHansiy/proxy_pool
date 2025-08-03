from fetcher.proxyFetcher import ProxyFetcher

if __name__ == '__main__':
    proxies = list(ProxyFetcher.freeProxy12(page_count=255))
    proxy_count = len(proxies)
    print(f'--- fetch freeProxy12 with 255 pages ---')
    print(f'Total proxies fetched: {proxy_count}')