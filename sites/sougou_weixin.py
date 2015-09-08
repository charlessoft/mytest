#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-08-12 16:00:09
# Project: sougou_weixin

from pyspider.libs.base_handler import *
from datetime import datetime

# 搜狗微信搜索 只能搜10页，  针对公众号 只能搜最近三个月的记录



class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://weixin.sogou.com/weixin?query=电力&type=2&ie=utf8', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        
        self.crawl(response.doc('a#sogou_next').attr.href, callback=self.index_page)
        
        items = []
        for each in response.doc('.txt-box').items():          
            items.append({
                'url':each('h4>a').attr.href,
                'title':each('h4>a').text(),
                'text':each('p').text(),
                'auther':each('div>a').attr.title,
                'create_time':each('div.s-p').attr.t
            })

        
        return items

