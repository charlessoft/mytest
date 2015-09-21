#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-08-10 11:32:41
# Project: SearchHandler

from pyspider.libs.base_handler import *
from udb_handler import UDBHandler
from helper import *
import time


class AccountHandler(UDBHandler):
    crawl_config = {
        'headers': {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        }
    }

    UPDATE_SETTINGS_INTERVAL = 3600
    LIST_ANCHOR_SEL = 'a.news_lst_tab'
    NEXT_ANCHOR_SEL = ''
    JS_ON = False

    def __init__(self):
        self.settings = {}

    def generate_urls(self):
        account_urls = dict()
        for account in self.get_accounts():
            account_urls[account] = self.build_url(account)
        return account_urls

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
        # self.target_urls = []
        if self.proxy_on:
            proxy_list = get_proxy_list()
            self.proxy_manager = ProxyManager(proxy_list)
        self.last_update_settings = time.time()

    @every(minutes=5)
    def on_start(self):
        self.check_settings()
        for account, url in self.generate_urls().items():
            context = {
                'account':account,
                'cur_page': 0,
            }
            self.crawl(url, callback=self.crawl_list_page, save=context, force_update=True)

    def crawl_list_page(self, response):
        for each in response.doc(self.LIST_ANCHOR_SEL).items():
            title = each.text().strip(' \n\r\t')
            if title and any(title.find(kw) > -1 for kw in self.get_keywords()):
                self.crawl(each.attr.href, callback=self.detail_page, bloomfilter_on=True)

    def get_keywords(self):
        # return []
        raise NotImplementedError

    def get_accounts(self):
        # return []
        raise NotImplementedError

    def build_url(self, keyword):
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