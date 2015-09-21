#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-09-14 15:24:15
# Project: sougou_weixin_openid

from pyspider.libs.base_handler import *
from handler.account_handler import AccountHandler as MyHandler
from pprint import pprint
 
class Handler(MyHandler):
    crawl_config = {
        'headers': {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        }
    }
    
    LIST_ANCHOR_SEL = 'a.news_lst_tab'
    NEXT_ANCHOR_SEL = 'xxx'
    JS_ON = True
    
    @every(minutes=5)
    def on_start(self):
        self.check_settings()
        for account, url in self.generate_urls().items():
            context = {
                'account':account,
                'cur_page': 0,
            }
            self.crawl(url, callback=self.crawl_list_page, fetch_type='js', save=context, force_update=True)

    def crawl_list_page(self, response):
        pprint(response.__dict__)
        for each in response.doc(self.LIST_ANCHOR_SEL).items():
            title = each.text().strip(' \n\r\t')
            if title and any(title.find(kw) > -1 for kw in self.get_keywords()):
                self.crawl(each.attr.href, callback=self.detail_page, cookies=response.cookies)
    
    def get_keywords(self):
        return [u'这', u'哈']

    def get_accounts(self):
        return ['oIWsFt2dA6-ADJmnDi1znkEYYw_M']

    def build_url(self, keyword):
        return 'http://weixin.sogou.com/gzh?openid=%s' % keyword

    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text().strip(),
            "text": response.doc('.rich_media_content').text().strip(),
            "publish_date": response.doc('#post-date').text(),
        }