#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-09-06 09:48:28
# Project: today_news
import re
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        }

    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://toutiao.com/', callback=self.index_page, fetch_type='js', js_script="""
                   function() {
                       window.scrollTo(0,document.body.scrollHeight);
                   }
                   """, force_update=True)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        print response.text
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page, fetch_type='js', js_script="""
                   function() {
                       window.scrollTo(0,document.body.scrollHeight);
                   }
                   """, force_update=True)

    @config(age=10 * 24 * 60 * 60)
    def list_page(self, response):
        #        for each in response.doc().items():
        #            print each
        for each in response.doc('html>body>#wrapper>#content>div>.article>div>.mod>.movie-list>dl>dd>A').items():
            # print each
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
