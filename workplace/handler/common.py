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
from udb_handler import UDBHandler
from atlproc import newspaperEngine

def get_proxy_list():
    proxy_list = []
    return proxy_list

def get_keywords():
    keywords = [u'电力', u'电网|尼玛']
    return keywords

def get_settings():
    target_urls = [
'http://www.chem17.com/offer_sale/detail/7156621.html',
'http://baozoumanhua.com/articles/3744536',
'http://www.cr-power.com/',
'http://shaoxing.19lou.com/forum-733-thread-114931414837769942-1-1.html',
'http://www.shumilou.com/chaojidianliqiangguo/',
'http://www.zepc.edu.cn/',
'http://www.tdqs.com/',
'http://www.nepcc4.com.cn/',
'http://www.nepco.net.cn/',
'http://www.ybzhan.cn/Product/detail/6485411.html',
'http://www.geta.org.cn/',
'http://www.contron.com.cn/',
        ]

    settings = {}

    for url in target_urls:
        settings[url] = {}
        settings[url]['proxy_on'] = False
        settings[url]['need_parse'] = False
        settings[url]['max_depth'] = 2

class ProxyManager(object):
    def __init__(self, proxies=[]):
        self.update(proxies)

    def update(self, proxies):
        self.proxies = list(proxies)
        self.record = {}
        self._cur = 0
        self._total = len(self.proxies)

    def pick_one(self):

        proxy = self.proxies[self._cur] if self._total > 0 else None
                
        if self._cur < self._total -1 :
            self._cur +=1
        else:
            self._cur = 0
        
        return proxy


class CommonSiteHandler(UDBHandler):
    crawl_config = {
        'headers': {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        }
    }

    UPDATE_SETTINGS_INTERVAL = 3600
    UPDATE_PROXIES_INTERVAL = 3600 * 12
    
    parser = newspaperEngine()

    def __init__(self):
        self.settings = {}
        self.proxy_manager = ProxyManager()

    def check_proxies(self):
        if time.time() - self.last_update_proxies > self.UPDATE_PROXIES_INTERVAL:
            self.update_proxies()

    def update_proxies(self):
        settings = getattr(self, 'settings', {})
        proxy_list = get_proxy_list()
        self.proxy_manager.update(proxy_list)
        self.last_update_proxies = time.time()

    def check_settings(self):
        if time.time() - self.last_update_settings > self.UPDATE_SETTINGS_INTERVAL:
            self.update_settings()

    def update_settings(self):
        settings = getattr(self, 'settings', {})

        new_settings = get_settings()
        for item in new_settings:
            domain = item['domain']
            del item['domain']
            settings[domain] = item
            # settings[domain]['proxy_on'] = item['proxy_on']
            # settings[domain]['need_parse'] = item['need_parse']
            # settings[domain]['max_depth'] = item['max_depth']
        self.settings = settings
        self.keywords = get_keywords()
        self.last_update_settings = time.time()

    def generate_urls(self):
        return self.settings.keys()

    def crawl(self, url, **kwargs):
        # if kwargs.get('save', {}).get('proxy_on', False):
        #     kwargs['proxy'] = self.proxy_manager.pick_one()
        hostname = kwargs.get('save', {}).get('hostname', None):
        if hostname:
            if self.settings.get(hostname, {}).get('proxy_on', False):
                kwargs['proxy'] = self.proxy_manager.pick_one()

        return super(CommonSiteHandler, self).crawl(url, **kwargs)

    @every(minutes=5)
    def on_start(self):
        self.check_settings()

        for url in self.generate_urls():
            parsed = urlparse(url)
            context = {
                'hostname': parsed.hostname,
                # 'proxy_on': self.settings[parsed.hostname]['proxy_on'],
                'cur_depth':self.max_depth,
            }
            self.crawl(url, callback=self.index_page, save=context, force_update=True)

    def index_page(self, response):
        cur_depth = response.save.get('cur_depth', 0)
        response.save['cur_depth'] = cur_depth -1

        if cur_depth:
            response.save['cur_depth'] = cur_depth -1
            for each in response.doc('a[href^="http"]').items():
                title = each.text().strip(' \n\r\t')
                if title and any(title.find(kw) > -1 for kw in self.keywords):
                    self.crawl(each.attr.href, callback=self.index_page, save=response.save)
        else:
            return self.parse(response)
            
            
    def parse(self, response):

        article = self.parser.parse(response.text)
    
        return {
            "url": response.url,
            "html": response.text,
            "title": article.title,
            "text": article.text,
            "authors": article.authors,
            "publish_date": article.publish_date,
            "top_img": article.top_img,
        }