#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mithril
# @Date:   2015-09-24 10:10:08
# @Last Modified by:   mithril
# @Last Modified time: 2015-11-19 11:03:02


from pyspider.libs.base_handler import every
from udbswp.handler.udb_handler import UDBHandler
from udbswp.handler.api import Api
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
    PROXY_ON = False
    JS_ON = False


    def generate_urls(self):
        kw_urls = dict()
        for keyword in self.keywords:
            kw_urls[keyword] = list(self.build_urls(keyword))
        return kw_urls

    def crawl_list_page(self, response):
        self.check(response)
        for each in response.doc(self.LIST_ANCHOR_SEL).items():
            self.crawl(each.attr.href, callback=self.detail_page, save=response.save, cookies=response.cookies, bloomfilter_on=True)

        self.crawl_next_page(response)

    def crawl_next_page(self, response):
        if response.save['cur_page'] < self.MAX_PAGE:
            response.save['cur_page'] += 1
            next_url = response.doc(self.NEXT_ANCHOR_SEL).attr.href
            if next_url:
                self.crawl(next_url, callback=self.crawl_list_page, save=response.save, cookies=response.cookies)

    @every(minutes=5)
    def on_start(self):
        ''' 可以将 self.check_update() 连同 on_start 移到UDBHandler，但是这样every 就不好设了'''
        self.check_update()
        kw_urls = self.generate_urls().items()
        for kw, urls in kw_urls:
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
        self.check(response)
        return {
            "url": response.url,
            "type": 'search',
            "title": response.doc('title').text(),
            "keyword": response.save.get('keyword')
        }

    def check(self, response):
        pass