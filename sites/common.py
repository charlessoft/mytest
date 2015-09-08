#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-08-30 11:32:41
# Project: common

from pyspider.libs.base_handler import *
from pyspider.libs.url import _build_url
from six.moves.urllib.parse import urlparse
import urllib
import requests
import time
from datetime import datetime

keywords = [u'电力', u'电网|尼玛']


def get_proxy_list():
    proxy_list = ['localhost:1080']
    return proxy_list

class ProxyManager(object):
    def __init__(self, proxies=[]):
        self.proxies = list(proxies)
        self.record = {}
        self._cur = 0
        self._total = len(self.proxies)

    def update(self):
        pass

    def pick_one(self):

        proxy = self.proxies[self._cur] if self._total > 0 else None
                
        if self._cur < self._total -1 :
            self._cur +=1
        else:
            self._cur = 0
        
        return proxy


class CommonSiteHandler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        }
    }

    UPDATE_SETTINGS_INTERVAL = 3600

    def __init__(self):
        self.last_update_settings = time.time()
        self.keywords = [u'电力', u'电网|尼玛']
        self.proxy_on = False
        self.max_recurrence = 3
        self.proxy_manager = {}
        self.target_urls = [
            'http://www.cepca.org.cn/',
            'http://www.chng.com.cn',
            'http://www.chder.com/',
            'http://www.bj.xinhuanet.com/power',
            'http://gu.qq.com/sh600795',
            'http://www.epae.cn/',
            'http://www.ceppea.net/',
            'http://ecp.sgcc.com.cn/',
            'http://www.shiep.edu.cn/',
            'http://www.cgdc.com.cn/',
            'http://www.cpnn.com.cn/cpnn_zt/csdjh/',
            'http://www.dlks.com.cn',
            'http://www.csg.cn/',
            'http://www.fj.95598.cn',
            'http://www.chinapowerbid.com/',
            'http://www.clypg.com.cn/',
            'http://www.cpicorp.com.cn/',
            'http://www.cpeinet.com.cn',
            'http://www.cecm.net.cn',
            'http://www.dl-maxonic.com/',
        ]

    def _need_update(self):
        return time.time() - self.last_update_settings > self.UPDATE_SETTINGS_INTERVAL

    def _update_settings(self):

        ''' get from server  '''

        self.proxy_on = True
        self.need_parse = True
        self.max_recurrence = 3
        self.keywords = [u'电力', u'电网|尼玛']
        # self.target_urls = []
        if self.proxy_on:
            proxy_list = get_proxy_list()
            self.proxy_manager = ProxyManager(proxy_list)
        self.last_update_settings = time.time()

    def crawl(self, url, **kwargs):
        if self._need_update():
            self._update_settings()

        if self.proxy_on:
            kwargs['proxy'] = self.proxy_manager.pick_one()

        return super(CommonSiteHandler, self).crawl(url, **kwargs)


    def on_start(self):
        self._update_settings()

        for url in self.target_urls:
            parsed = urlparse(url)
            context = {
                'hostname': parsed.hostname,
                'cur_recurrence':self.max_recurrence
            }
            self.crawl(url, callback=self.index_page, save=context, force_update=True)


    def index_page(self, response):
        cur_recurrence = response.save.get('cur_recurrence', 0)
        response.save['cur_recurrence'] = cur_recurrence -1

        if cur_recurrence:
            response.save['cur_recurrence'] = cur_recurrence -1
            for each in response.doc('a[href^="http"]').items():
                title = each.text().strip(' \n\r\t')
                if title and any(title.find(kw) > -1 for kw in keywords):
                    self.crawl(each.attr.href, callback=self.index_page, save=response.save)
        else:
            return {
                "url": response.url,
                "title": response.doc('title').text(),
                "text": response.text,
            }
