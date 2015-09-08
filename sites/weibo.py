#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-08-19 16:01:28
# Project: weibo

# 只有50页

# 实际观察是quote 了2次 如下， 不过使用quote一次也能搜
# http://s.weibo.com/weibo/%25E7%2594%25B5%25E5%258A%259B&page=2


from pyspider.libs.base_handler import *
from urllib import quote
from weibo.login import WeiboLogin, WeiboLoginFailure
import requests

username = 'androidq@sina.cn'
passwd = 'azsx123'


l = WeiboLogin(username, passwd)
l.login()

weibo_cookies = requests.utils.dict_from_cookiejar(l.session.cookies)


class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        },
        'cookies': weibo_cookies
    }

    @every(minutes=10)
    def on_start(self):
        self.crawl('http://s.weibo.com/weibo/%25E7%2594%25B5%25E5%258A%259B', 
                   fetch_type='js', js_script="""
                   function() {
                       window.scrollTo(0,document.body.scrollHeight);
                   }
                   """, callback=self.index_page, force_update=True)

        
    def index_page(self, response):
        
        self.crawl(response.doc('.page.next').attr('href'), fetch_type='js', js_script="""
                   function() {
                       window.scrollTo(0,document.body.scrollHeight);
                   }
                   """, callback=self.index_page, force_update=True)
              
        results = []
        for each in response.doc('.content.clearfix').items():
            date_elem = each.find('.feed_from a[suda-data]')
            results.append({
                'nick_name': each.find('.W_texta').attr('nick-name'),
                'text': each.find('.comment_txt').text(),
                'date': date_elem.attr('date'),
                'url': date_elem.attr('href'),
            })
            
        return results
            
    def check(self, dest_url):
        if dest_url.startswith('http://weibo.com/login.php'):
            raise WeiboLoginFailure('Weibo not login or login expired')
        if dest_url.startswith('http://weibo.com/sorry?usernotexists'):
            self.bundle.exists = False
            return False
        return True

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
