#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-08-19 14:43:02
# Project: souguo

from pyspider.libs.base_handler import *
from lxml import html
from six.moves.urllib.parse import urlparse

# 最多 100 页
# 说是每分钟更新

# interation=196648 这个参数指定 搜索类型

# pyquery 只能取到 news的前 2个a
# 应该是解码的时候第三个a 前有 <!--resulttitle:�十大�明星脸！好声音变成全明星“撞脸大会”-->
# 乱码导致无法解码 直接用lxml 

first_or_none = lambda x:x[0] if len(x) else None

sougou_dict = {
    'news': 'http://news.sogou.com/news?&clusterId=&p=42230305&time=0&query=%CA%AE%B4%F3&mode=1&media=&sort=1',
    'bbs': 'http://www.sogou.com/web?query=%E8%A2%AB%E4%BB%A3%E8%A1%A8&_asf=www.sogou.com&interation=196648',
    'blog': 'http://www.sogou.com/web?query=%E8%A2%AB%E4%BB%A3%E8%A1%A8&_asf=www.sogou.com&interation=196647'
}

class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        }
    }
    
    
    @every(minutes=24 * 60)
    def on_start(self):
        url = sougou_dict['news']
        parsed = urlparse(url)
        save = {
            'host': 'http://' + parsed.hostname + parsed.path
        }
        self.crawl(sougou_dict['news'], callback=self.index_page, save=save, force_update=True)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        h = html.fromstring(response.text)

        for url in h.xpath('//a[@class="pp"]/@href'):
            self.crawl(url, callback=self.detail_page)
        #for each in response.doc('h3>a').items():
        #    self.crawl(each.attr('href'), callback=self.detail_page)
            
        url = first_or_none(h.xpath('//a[@class="np"]/@href'))
        self.crawl(response.save.get('host', '') + url, callback=self.index_page, save=response.save, force_update=True)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
