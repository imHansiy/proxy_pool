# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test.py  
   Description :  
   Author :       JHao
   date：          2017/3/7
-------------------------------------------------
   Change Activity:
                   2017/3/7: 
-------------------------------------------------
"""
__author__ = 'JHao'

import unittest

if __name__ == '__main__':
    # 创建一个测试加载器
    loader = unittest.TestLoader()
    
    # 从 "test" 目录中发现所有测试
    suite = loader.discover('test')
    
    # 创建一个测试运行器
    runner = unittest.TextTestRunner()
    
    # 运行测试套件
    runner.run(suite)
