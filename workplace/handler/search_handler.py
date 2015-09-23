#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-08-10 11:32:41
# Project: SearchHandler

from pyspider.libs.base_handler import every
from handler.udb_handler import UDBHandler
from handler.api import Api
import time


class SearchHandler(UDBHandler):
    crawl_config = {
        'headers': {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        }
    }

    UPDATE_SETTINGS_INTERVAL = 3600
    UPDATE_KEYWORDS_INTERVAL = 3600
    UPDATE_PROXIES_INTERVAL = 3600*12
    MAX_PAGE = 5
    LIST_ANCHOR_SEL = 'h3>a'
    NEXT_ANCHOR_SEL = 'a#next'

    def generate_urls(self):
        kw_urls = dict()
        for keyword in self.keywords:
            kw_urls[keyword] = list(self.build_urls(keyword))
        return kw_urls

    def crawl_list_page(self, response):
        for each in response.doc(self.LIST_ANCHOR_SEL).items():
            self.crawl(each.attr.href, callback=self.detail_page, bloomfilter_on=True)

        self.crawl_next_page(response)

    def crawl_next_page(self, response):
        if response.save['cur_page'] < self.MAX_PAGE:
            response.save['cur_page'] += 1
            next_url = response.doc(self.NEXT_ANCHOR_SEL).attr.href
            if next_url:
                self.crawl(next_url, callback=self.crawl_list_page, save=response.save, bloomfilter_on=True)

    @every(minutes=5)
    def on_start(self):
        ''' 可以将 self.check_update() 连同 on_start 移到UDBHandler，但是这样every 就不好设了'''
        self.check_update()
        for kw, urls in self.generate_urls().items():
            context = {
                'keyword':kw,
                'cur_page': 0,
            }
            for url in urls:
                self.crawl(url, callback=self.crawl_list_page, save=context, force_update=True)

    def build_urls(self, keyword):
        '''
        1. return self.build_url(keyword, page_num) for page_num in xrange(max_page)
        2. return self.build_url(keyword)
        '''
        raise NotImplementedError

    def detail_page(self, response):
        return {
            "url": response.url,
            "type": 'search',
            "title": response.doc('title').text(),
            "keyword": response.save.get('keyword')
        }
