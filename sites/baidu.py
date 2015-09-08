#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-08-10 11:32:41
# Project: baidu

from pyspider.libs.base_handler import *
from pyspider.libs.url import _build_url
import urllib
import requests

# 百度最多只有76页
keywords = ['电力', '电网|尼玛']


def build_baidu_url(word, page):
    baidu_base_url = 'http://www.baidu.com/s?'
    qs_dict = {'wd':word,'pn':str(page)+'0','tn':'baidurt','ie':'utf-8','bsst':'1'}
    return _build_url(baidu_base_url, qs_dict)

    
class baidu_urls:
    def __init__(self, word, max_page=1):
        self.base_url = 'http://www.baidu.com/s?'
        self.cur = 0
        self.word = word
        self.max_page = max_page
        
    def __iter__(self):
        return self

    def next(self):
        if self.cur < self.max_page:
            urls = build_baidu_url(self.word, self.cur)
            self.cur += 1
            return urls
        else:
            raise StopIteration()
    
    
class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        }
    }

    @every(minutes=5)
    def on_start(self):
        for kw in keywords:
            self.crawl(baidu_urls(kw, 5), callback=self.index_page, 
                        save=kw, force_update=True)
        
    def index_page(self, response):
        for each in response.doc('h3>a').items():
            self.crawl(each.attr.href, callback=self.detail_page, bloomfilter_on=True)
            
        # 会在00 和10 之间循环
        # next_url = response.doc('a.n').attr.href
        # page_cur = response.save+1
        # self.crawl(build_baidu_url('电力', page_cur), callback=self.index_page, save=page_cur, ignore_filter=True, force_update=True)

    @config(priority=1)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
