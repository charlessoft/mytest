#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-09-01 16:23:31
# Project: yr_oa

from pyspider.libs.base_handler import *

from yr_login.yr_oa_login import *
import re
yr_oa = YRLogin()
yr_oa.set_userinfo(username, password)
#session = yr_oa.login()
#yr_oa_cookies = requests.utils.dict_from_cookiejar(session.cookies)

class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        },
        "cookies": {
            "LtpaToken": "AAECAzU1RTU3MkMyNTVFNUI5MTJDTj0Ts8ITx6MvTz0T0toT6cUT0MUTz6IlgLIO4VuJQjrdwRKbF3A4CVxpxQ=="

        }
        #'cookies': yr_oa_cookies
    }
    def __init__(self):
        BaseHandler.__init__(self)
        self.m_date = 'sssda'

    @every(minutes=24 * 60)
    def on_start(self):
        #print session.cookies
        self.crawl('http://oa.yirong-info.com:8000/pt_index.htm', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        #print response.doc
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.load_chanel_page)

    @config(age=10 * 24 * 60 * 60)
    def load_chanel_page(self, response):

        pattern = r"Ajax.loadXml\('(.*)'"
        m = re.search(pattern,response.content)
        if m:
            print m.groups()[0]
            self.crawl(m.groups()[0], callback=self.load_xml_page)
        else:
            print "no"


    @config(age=10 * 24 * 60 * 60)
    def load_xml_page(self, response):
        for each in response.doc('Item').items():
            url = 'http://oa.yirong-info.com:8000' + each('url').text()
            #print 'http://oa.yirong-info.com:8000'+url
            self.crawl(url, callback=self.detail_page)



    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
