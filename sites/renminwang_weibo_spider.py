#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-09-19 14:53:54
# Project: renmingwang_webo

from pyspider.libs.base_handler import *
from renminwang_weibo_login import renmin_weibo_login
import requests
username = 'studio20130101'
passwd = 'aA123456789'

#session = requests.Session()
#session.headers = {
#    'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 #Safari/537.36',
#}

renmin_login = renmin_weibo_login.renmin_login()
renmin_login.forwardIndex_action()
renmin_login.userAccessLog_action()
renmin_login.login_action()

#l = WeiboLogin(session, username, passwd)
#l.login()


renmin_cookies = requests.utils.dict_from_cookiejar(renmin_login.m_session.cookies)
print renmin_cookies



class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        },
        'cookies':renmin_cookies
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://t.people.com.cn/searchV3.action?searchInput=%B5%E7%C1%A6', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        results = []
        for each in response.doc('.WBM_list>div').items():
            publish_date = each.find('.list_detail>.skin_color_02>.list_time').find('a').eq(0).text()
            results.append({
                'nickname':each.find('.list_name').attr('data-nickname'),
                'text':each.find('.list_detail>.skin_color_01>span').text(),
                'publish_date':publish_date,
                'from':each.find('.list_detail>.skin_color_02>.list_time').text().replace(publish_date,'').replace(u'来自','').strip(' \r\n\t')}
            )
        return results





        #for each in response.doc('a[href^="http"]').items():
        #    self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
