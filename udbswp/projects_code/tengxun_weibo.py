#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-11-02 11:37:22
# Project: tengxun_weibo

from pyspider.libs.base_handler import *
from pyspider.libs.base_handler import *
from urllib import quote
from udbswp.handler.search_handler import SearchHandler as MyHandler
from udbswp.login.tencent_weibo_login.tencent_weibo_login import *
import requests
import sys

#from sites.teng_xun_login.tencent_weibo_login import *

username = '295044696'
password = 'aA1234567890'
# account_hex = '\x00\x00\x00\x00\x11\x96\x06\x58'
weibo = tencent_weibo_login()
weibo.set_userinfo(username, password)
cookie = weibo.qqlogin()



class Handler(MyHandler):
    crawl_config = {
        'headers': {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
'cookie':cookie
        }
    }

    def build_urls(self, keyword):
       print keyword
       return ['http://search.t.qq.com/index.php?k=%s&pos=174&s_source=' % keyword]


    @every(minutes=1)
    def on_start(self):
        self.check_update()

        kw_urls = self.generate_urls().items()
        for kw, urls in kw_urls:
            context = {
                'keyword':kw,

            }
            for url in urls:

                self.crawl(url, fetch_type='js', js_script="""
                   function() {
                       window.scrollTo(0,document.body.scrollHeight);
                   }
                   """,callback=self.crawl_list_page, save=context, force_update=True)




    def crawl_list_page(self,response):
        for each in response.doc('.LC').find('li').items():

            yield {
                "title" : each('.msgBox').children('.userName')('a').attr('title'),
                "url":each(".mFun")('div>p>a').eq(1).attr.href,
                "like_num":each('.msgBox')('.funBox')("a>span").text(),
                "publish_time":each('.msgBox')('.time').attr("rel"),
                "content":(each)('.msgBox')('.msgCnt').text()
            }



