#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-09-16 15:32:10
# Project: xinhuawang_weibo

#新华网不需要登陆。
from pyspider.libs.base_handler import *

from pyquery import PyQuery as pq
class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://t.home.news.cn/dirMblogByTrs.action?pageTag=0&pageType=1&serchType=&keyword2=&keyword3=&keyword4=&keyword1=%E6%94%B9%E9%9D%A9%E5%BC%80%E6%94%BE', callback=self.index_page,fetch_type='js')

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        results = []
        for each in response.doc(".LC").items():
            li_list = each.find("li")
            for li_item in li_list:
                xinhua_article = {}
                xinhua_article["userName"] = pq(li_item).find(".userName").find("a").attr("title")
                xinhua_article["msgCnt"] = pq(li_item).find(".msgCnt").text()
                xinhua_article["pubInfo"] = pq(li_item).find(".pubInfo").find("a").attr("title")
                results.append(xinhua_article)
        return results

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
