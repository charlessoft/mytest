#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-08-10 11:32:41
# Project: SearchHandler

from pyspider.libs.base_handler import every
from handler.udb_handler import UDBHandler
import time

class AccountHandler(UDBHandler):
    crawl_config = {
        'headers': {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        }
    }

    UPDATE_SETTINGS_INTERVAL = 3600
    UPDATE_KEYWORDS_INTERVAL = 3600
    UPDATE_PROXIES_INTERVAL = 3600*12
    UPDATE_ACCOUNTS_INTERVAL = 3600
    LIST_ANCHOR_SEL = 'a.news_lst_tab'
    NEXT_ANCHOR_SEL = ''
    JS_ON = False
    ACCOUNT_TYPE = None

    def __init__(self):
        super(AccountHandler, self).__init__()
        self.update_accounts()

    def check_update(self):
        super(AccountHandler, self).check_update()
        if time.time() - self.last_update_accounts > self.UPDATE_ACCOUNTS_INTERVAL:
            self.update_accounts()

    def update_accounts(self):
        self.accounts = self.api.get_accounts(tp=self.ACCOUNT_TYPE)
        self.last_update_accounts = time.time()

    def generate_urls(self):
        account_urls = dict()
        for account in self.accounts:
            account_urls[account] = self.build_url(account)
        return account_urls

    @every(minutes=5)
    def on_start(self):
        self.check_update()
        for account, url in self.generate_urls().items():
            context = {
                'account':account,
                'cur_page': 0,
            }
            self.crawl(url, callback=self.crawl_list_page, save=context, force_update=True)

    def crawl_list_page(self, response):
        for each in response.doc(self.LIST_ANCHOR_SEL).items():
            title = each.text().strip(' \n\r\t')
            if title and any(title.find(kw) > -1 for kw in self.keywords):
                self.crawl(each.attr.href, callback=self.detail_page, save=response.save, bloomfilter_on=True)

    def build_url(self, account):
        '''
        '''
        raise NotImplementedError

    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
            "type": 'account',
            "authors": response.save.get('account'),
        }