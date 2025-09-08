# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxyScheduler
   Description :
   Author :        JHao
   date：          2019/8/5
-------------------------------------------------
   Change Activity:
                   2019/08/05: proxyScheduler
                   2021/02/23: runProxyCheck时,剩余代理少于POOL_SIZE_MIN时执行抓取
-------------------------------------------------
"""
__author__ = 'JHao'

import time
from util.six import Queue
from helper.fetch import Fetcher
from helper.check import Checker
from handler.logHandler import LogHandler
from handler.proxyHandler import ProxyHandler
from handler.configHandler import ConfigHandler


def __runProxyFetch():
    proxy_queue = Queue()
    proxy_fetcher = Fetcher()

    for proxy in proxy_fetcher.run():
        proxy_queue.put(proxy)

    Checker("raw", proxy_queue)


def __runProxyCheck():
    proxy_handler = ProxyHandler()
    proxy_queue = Queue()
    if proxy_handler.db.getCount().get("total", 0) < proxy_handler.conf.poolSizeMin:
        __runProxyFetch()
    for proxy in proxy_handler.getAll():
        proxy_queue.put(proxy)
    Checker("use", proxy_queue)


def runScheduler(now=False):
    if now:
        __runProxyCheck()
        return

    log = LogHandler("scheduler")
    log.info("Starting scheduler...")

    conf = ConfigHandler()

    while True:
        log.info("Starting proxy fetch...")
        __runProxyFetch()
        log.info("Proxy fetch finished.")

        log.info("Starting proxy check...")
        __runProxyCheck()
        log.info("Proxy check finished.")

        log.info(f"Scheduler sleeping for {conf.fetcherInterval} seconds...")
        time.sleep(conf.fetcherInterval)


if __name__ == '__main__':
    runScheduler()
