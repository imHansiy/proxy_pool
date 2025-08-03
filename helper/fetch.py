# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     fetchScheduler
   Description :
   Author :        JHao
   date：          2019/8/6
-------------------------------------------------
   Change Activity:
                   2021/11/18: 多线程采集
-------------------------------------------------
"""
__author__ = 'JHao'

from threading import Thread
from helper.proxy import Proxy
from helper.check import DoValidator
from handler.logHandler import LogHandler
from handler.proxyHandler import ProxyHandler
from fetcher.proxyFetcher import ProxyFetcher
from handler.configHandler import ConfigHandler


class _ThreadFetcher(Thread):

    def __init__(self, fetch_source, proxy_dict):
        Thread.__init__(self)
        self.fetch_source = fetch_source
        self.proxy_dict = proxy_dict
        self.fetcher = getattr(ProxyFetcher, fetch_source, None)
        self.log = LogHandler("fetcher")
        self.conf = ConfigHandler()
        self.proxy_handler = ProxyHandler()

    def run(self):
        self.log.info("ProxyFetch - {func}: start".format(func=self.fetch_source))
        try:
            for proxy in self.fetcher():
                if isinstance(proxy, dict):
                    self.log.info(f'ProxyFetch - {self.fetch_source}: {proxy["ip"]}:{proxy["port"]} ok')
                    p = Proxy(f'{proxy["ip"]}:{proxy["port"]}', source=self.fetch_source, protocol=proxy["protocol"])
                else:
                    self.log.info(f'ProxyFetch - {self.fetch_source}: {proxy.ljust(23)} ok')
                    proxy = proxy.strip()
                    p = Proxy(proxy, source=self.fetch_source)

                if p.proxy in self.proxy_dict:
                    self.proxy_dict[p.proxy].add_source(self.fetch_source)
                else:
                    self.proxy_dict[p.proxy] = p
        except Exception as e:
            self.log.error("ProxyFetch - {func}: error".format(func=self.fetch_source))
            self.log.error(str(e))


class Fetcher(object):
    name = "fetcher"

    def __init__(self):
        self.log = LogHandler(self.name)
        self.conf = ConfigHandler()

    def run(self):
        """
        fetch proxy with proxyFetcher
        :return:
        """
        proxy_dict = dict()
        thread_list = list()
        self.log.info("ProxyFetch : start")

        for fetch_source in self.conf.fetchers:
            self.log.info("ProxyFetch - {func}: start".format(func=fetch_source))
            fetcher = getattr(ProxyFetcher, fetch_source, None)
            if not fetcher:
                self.log.error("ProxyFetch - {func}: class method not exists!".format(func=fetch_source))
                continue
            if not callable(fetcher):
                self.log.error("ProxyFetch - {func}: must be class method".format(func=fetch_source))
                continue
            thread_list.append(_ThreadFetcher(fetch_source, proxy_dict))

        for thread in thread_list:
            thread.setDaemon(True)
            thread.start()

        for thread in thread_list:
            thread.join()

        self.log.info("ProxyFetch - all complete!")
        for _ in proxy_dict.values():
            if DoValidator.preValidator(_.proxy):
                yield _
