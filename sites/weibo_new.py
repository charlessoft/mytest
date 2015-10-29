#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mithril
# @Date:   2015-10-28 15:35:42
# @Last Modified by:   mithril
# @Last Modified time: 2015-10-28 15:35:51


# 只有50页

# 实际观察是quote 了2次 如下， 不过使用quote一次也能搜
# http://s.weibo.com/weibo/%25E7%2594%25B5%25E5%258A%259B&page=2


from pyspider.libs.base_handler import *
from urllib import quote
from udbswp.handler.search_handler import SearchHandler as MyHandler
from lxml import html
from pyquery import PyQuery as pq
import requests
import time
import json



class Handler(MyHandler):
    crawl_config = {
        'headers': {
            'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
        }
    }


    PROXY_ON = True
    JS_ON = False


    def build_urls(self, keyword):
        return ['http://s.weibo.com/weibo/%s' % keyword]


    @every(minutes=10)
    def on_start(self):
        sleep_interval = 20
        i = 0
        self.check_update()
        kw_urls = self.generate_urls().items()
        for kw, urls in kw_urls:
            context = {
                'keyword':kw,
                'cur_page': 0,
            }
            for url in urls:
                self.crawl(url, callback=self.crawl_list_page, exetime=time.time() + sleep_interval*i, save=context, force_update=True)
                i +=1


    def crawl_list_page(self, response):
        self.check(response)

        target = response.xdoc.xpath('//script[contains(text(), "pl_weibo_direct")]')[-1]
        json_data = target.text_content().replace('STK && STK.pageletM && STK.pageletM.view','').strip('()')
        data = json.loads(json_data)
        doc = pq(html.fromstring(data['html']))

        for each in doc('.content.clearfix').items():
            date_elem = each.find('.feed_from a[suda-data]')
            yield {
                'type':'sina_weibo',
                'authors': each.find('.W_texta').attr('nick-name'),
                'text': each.find('.comment_txt').text(),
                'publish_time': int(date_elem.attr('date'))/1000,
                'url': date_elem.attr('href'),
            }


    def check(self, response):
        if response.doc('.code_tit'):
            print response.text
            raise Exception('sina weibo require captcha!')

        if response.url.startswith('http://weibo.com/login.php'):
            raise WeiboLoginFailure('Weibo not login or login expired')
        if response.url.startswith('http://weibo.com/sorry?usernotexists'):
            self.bundle.exists = False
            return False
        return True

