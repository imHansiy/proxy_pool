# -*- coding: utf-8 -*-
from fetcher.proxyFetcher import ProxyFetcher

def test_freeProxy12():
    """
    Test freeProxy12 fetcher
    """
    fetcher = ProxyFetcher()
    count = 0
    for proxy in fetcher.freeProxy12():
        print(proxy)
        assert proxy.proxy is not None
        count += 1
    assert count > 0

if __name__ == '__main__':
    test_freeProxy12()