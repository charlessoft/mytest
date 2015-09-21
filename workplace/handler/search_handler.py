#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-08-10 11:32:41
# Project: SearchHandler

from pyspider.libs.base_handler import *
from pyspider.libs.url import _build_url
from udb_handler import UDBHandler
from helper import *
import time


class SearchHandler(UDBHandler):
    crawl_config = {
        'headers': {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        }
    }

    UPDATE_SETTINGS_INTERVAL = 3600
    MAX_PAGE = 5
    LIST_ANCHOR_SEL = 'h3>a'
    NEXT_ANCHOR_SEL = 'a#next'

    def __init__(self):
        self.settings = {}

    def generate_urls(self):
        kw_urls = dict()
        for keyword in self.keywords:
            kw_urls[keyword] = list(self.build_urls(keyword))
        return kw_urls
        
    def loop(self, response):
        self.crawl_list_page(response)
        if response.save['cur_page'] < self.MAX_PAGE:
            response.save['cur_page'] +=1
            self.crawl_next_page(self, response)

    def crawl_list_page(self, response):
        for each in response.doc(self.LIST_ANCHOR_SEL).items():
            self.crawl(each.attr.href, callback=self.detail_page, bloomfilter_on=True)

    def crawl_next_page(self, response, callback):
        next_url = response.doc(self.NEXT_ANCHOR_SEL).attr.href
        if next_url:
            self.crawl(next_url, callback=self.loop, bloomfilter_on=True)

    def check_settings(self):
        if not hasattr(self, 'last_update_settings'):
            self.update_settings()
        elif time.time() - self.last_update_settings > self.UPDATE_SETTINGS_INTERVAL:
            self.update_settings()

    def update_settings(self):
        ''' get from server  '''
        self.proxy_on = True
        self.need_parse = True
        self.max_depth = 3
        self.keywords = [u'电力', u'电网|尼玛']
        # self.target_urls = []
        if self.proxy_on:
            proxy_list = get_proxy_list()
            self.proxy_manager = ProxyManager(proxy_list)
        self.last_update_settings = time.time()

    @every(minutes=5)
    def on_start(self):
        self.check_settings()
        for kw, urls in self.generate_urls().items():
            context = {
                'keyword':kw,
                'cur_page': 0,
            }
            for url in urls:
                self.crawl(url, callback=self.loop, save=context, force_update=True)

    def build_urls(self, keyword):
        '''
        1. return self.build_url(keyword, page_num) for page_num in xrange(max_page)
        2. return self.build_url(keyword)
        '''
        raise NotImplementedError

    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
            "keyword": response.save.get('keyword')
        }