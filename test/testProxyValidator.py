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
from helper.validator import ProxyValidator


class TestProxyValidator(unittest.TestCase):

    @patch('helper.validator.socksTimeOutValidator')
    def test_socks_validation(self, mock_socks_validator):
        # 模拟代理对象
        proxy_socks5 = Proxy.createFromJson('{"proxy": "127.0.0.1:1080", "protocol": "socks5"}')
        proxy_socks4 = Proxy.createFromJson('{"proxy": "127.0.0.1:1081", "protocol": "socks4"}')

        # 场景1: SOCKS5 验证成功
        mock_socks_validator.return_value = True
        # 模拟验证器执行
        result = all(func(proxy_socks5.uri) for func in ProxyValidator.socks_validator)
        self.assertTrue(result)
        mock_socks_validator.assert_called_with(proxy_socks5.uri)
        mock_socks_validator.reset_mock()

        # 场景2: SOCKS4 验证成功
        mock_socks_validator.return_value = True
        result = all(func(proxy_socks4.uri) for func in ProxyValidator.socks_validator)
        self.assertTrue(result)
        mock_socks_validator.assert_called_with(proxy_socks4.uri)
        mock_socks_validator.reset_mock()

        # 场景3: SOCKS5 验证失败
        mock_socks_validator.return_value = False
        result = all(func(proxy_socks5.uri) for func in ProxyValidator.socks_validator)
        self.assertFalse(result)
        mock_socks_validator.assert_called_with(proxy_socks5.uri)
        mock_socks_validator.reset_mock()

        # 场景4: SOCKS4 验证失败
        mock_socks_validator.return_value = False
        result = all(func(proxy_socks4.uri) for func in ProxyValidator.socks_validator)
        self.assertFalse(result)
        mock_socks_validator.assert_called_with(proxy_socks4.uri)


if __name__ == '__main__':
    unittest.main()
