#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-09-14 15:24:15
# Project: sougou_weixin_openid

from pyspider.libs.base_handler import *
from handler.account_handler import AccountHandler as MyHandler
from weibo.login import WeiboLogin, WeiboLoginFailure
from pprint import pprint
import requests
 
    
username = 'androidq@sina.cn'
passwd = 'azsx123'


l = WeiboLogin(username, passwd)
l.login()

weibo_cookies = requests.utils.dict_from_cookiejar(l.session.cookies)
    
class Handler(MyHandler):
    crawl_config = {
        'headers': {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        },
        'cookies': weibo_cookies
    }
    
    LIST_ANCHOR_SEL = 'a.news_lst_tab'
    NEXT_ANCHOR_SEL = 'xxx'
    JS_ON = True
    
    @every(minutes=5)
    def on_start(self):
        self.check_settings()
        for account, url in self.generate_urls().items():
            context = {
                'account':account,
                'cur_page': 0,
            }
            self.crawl(url, callback=self.crawl_list_page, fetch_type='js', save=context, force_update=True)

    def crawl_list_page(self, response):
        results = []
        for each in response.doc('.WB_feed_detail').items():
            date_elem = each.find('[node-type="feed_list_item_date"]')
            results.append({
                'nick_name': response.save.get('account'),
                'text': each.find('.WB_detail').text(), # or .WB_text
                'date': date_elem.attr('title'), # or date  1440756811000
                'url': date_elem.attr('href'),
            })
            
        return results
    
    def get_keywords(self):
        return [u'这', u'好']

    def get_accounts(self):
        return ['realangelababy']

    def build_url(self, account):
        return 'http://weibo.com/%s' % account

    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text().strip(),
            "text": response.doc('.rich_media_content').text().strip(),
            "publish_date": response.doc('#post-date').text(),
        }