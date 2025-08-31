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
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch, MagicMock
import requests
from helper.proxy import Proxy
from helper.validator import httpTimeOutValidator, httpsTimeOutValidator, ProxyValidator


class TestProxyValidator(unittest.TestCase):

    @patch('helper.validator.get')
    def test_http_validation(self, mock_get):
        # 场景1: 验证成功
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ip": "127.0.0.1"}
        mock_get.return_value = mock_response
        self.assertTrue(httpTimeOutValidator("127.0.0.1:8080"))

        # 场景2: 状态码不为200
        mock_response.status_code = 500
        self.assertFalse(httpTimeOutValidator("127.0.0.1:8080"))

        # 场景3: 请求异常
        mock_get.side_effect = requests.exceptions.RequestException
        self.assertFalse(httpTimeOutValidator("127.0.0.1:8080"))

    @patch('helper.validator.get')
    def test_https_validation(self, mock_get):
        # 场景1: 验证成功
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ip": "127.0.0.1"}
        mock_get.return_value = mock_response
        self.assertTrue(httpsTimeOutValidator("127.0.0.1:8080"))

        # 场景2: 状态码不为200
        mock_response.status_code = 500
        self.assertFalse(httpsTimeOutValidator("127.0.0.1:8080"))

        # 场景3: 请求异常
        mock_get.side_effect = requests.exceptions.RequestException
        self.assertFalse(httpsTimeOutValidator("127.0.0.1:8080"))

    @patch('helper.validator.head')
    def test_socks_validation(self, mock_head):
        # 模拟代理对象
        proxy_socks5 = Proxy.createFromJson('{"proxy": "127.0.0.1:1080", "protocol": "socks5"}')
        proxy_socks4 = Proxy.createFromJson('{"proxy": "127.0.0.1:1081", "protocol": "socks4"}')

        # 场景1: SOCKS5 验证成功
        mock_head.return_value.status_code = 200
        # 模拟验证器执行
        for func in ProxyValidator.socks_validator:
            self.assertTrue(func(proxy_socks5))

        # 场景2: SOCKS4 验证成功
        mock_head.return_value.status_code = 200
        for func in ProxyValidator.socks_validator:
            self.assertTrue(func(proxy_socks4))

        # 场景3: SOCKS5 验证失败
        mock_head.return_value.status_code = 500
        for func in ProxyValidator.socks_validator:
            self.assertFalse(func(proxy_socks5))

        # 场景4: SOCKS4 验证失败
        mock_head.return_value.status_code = 500
        for func in ProxyValidator.socks_validator:
            self.assertFalse(func(proxy_socks4))


if __name__ == '__main__':
    unittest.main()
