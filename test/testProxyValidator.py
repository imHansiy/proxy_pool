# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     testProxyValidator
   Description :
   Author :        JHao
   date：          2021/5/25
-------------------------------------------------
   Change Activity:
                   2021/5/25:
-------------------------------------------------
"""
__author__ = 'JHao'

import unittest
from unittest.mock import patch
import requests
from helper.proxy import Proxy
from helper.validator import socksTimeOutValidator, ProxyValidator


class TestProxyValidator(unittest.TestCase):

    def test_socks_validation(self):
        # 模拟代理对象
        proxy_socks5_success = Proxy.createFromJson({'proxy': '127.0.0.1:1080', 'proxy_type': 'socks5'})
        proxy_socks4_success = Proxy.createFromJson({'proxy': '127.0.0.1:1081', 'proxy_type': 'socks4'})
        proxy_timeout = Proxy.createFromJson({'proxy': '127.0.0.1:1082', 'proxy_type': 'socks5'})
        proxy_conn_error = Proxy.createFromJson({'proxy': '127.0.0.1:1083', 'proxy_type': 'socks4'})

        # 模拟网络请求
        with patch('requests.get') as mock_get:
            # 模拟成功的SOCKS5代理验证
            mock_get.return_value.status_code = 200
            self.assertTrue(socksTimeOutValidator(proxy_socks5_success))

            # 模拟成功的SOCKS4代理验证
            self.assertTrue(socksTimeOutValidator(proxy_socks4_success))

            # 模拟因超时导致的验证失败
            mock_get.side_effect = requests.exceptions.Timeout
            self.assertFalse(socksTimeOutValidator(proxy_timeout))

            # 模拟因连接错误导致的验证失败
            mock_get.side_effect = requests.exceptions.ConnectionError
            self.assertFalse(socksTimeOutValidator(proxy_conn_error))


def testProxyValidator():
    for _ in ProxyValidator.pre_validator:
        print(_)
    for _ in ProxyValidator.http_validator:
        print(_)
    for _ in ProxyValidator.https_validator:
        print(_)


if __name__ == '__main__':
    testProxyValidator()
