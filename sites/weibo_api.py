#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-11-12 16:14:32
# Project: weibo_api

from pyspider.libs.base_handler import *
from udbswp.handler.search_handler import SearchHandler as MyHandler




class Handler(MyHandler):
    crawl_config = {
        'headers': {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
        }
    }


    def build_urls(self, keyword):
        return ['http://wyxmobilecenter.appsina.com/api/search?q=%s&page=1&count=50' % keyword]

    @every(minutes=10)
    def on_start(self):

        self.check_update()
        kw_urls = self.generate_urls().items()
        for kw, urls in kw_urls:
            context = {
                'keyword':kw,
                'cur_page': 0,
            }
            for url in urls:
                self.crawl(url, callback=self.detail_page, force_update=True)


    @config(priority=2)
    def detail_page(self, response):
        for post in response.json['statuses']:
            yield {
                'url':post['id'],
                'publish_time':post['created_at'],
                'text':post['text'],
                'author':post['user']['name'],
            }
