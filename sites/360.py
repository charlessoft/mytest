#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-08-19 14:34:53
# Project: 360

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=5)
    def on_start(self):
        self.crawl('http://www.haosou.com/s?ie=utf-8&shb=1&src=360sou_newhome&q=%E7%94%B5%E5%8A%9B', 
                   callback=self.index_page, force_update=True)

    def index_page(self, response):
        for each in response.doc('.res-title > a').items():
            self.crawl(each.attr.href, callback=self.detail_page)
            
        self.crawl(response.doc('#snext').attr.href, callback=self.index_page, force_update=True)
        

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
