#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-08-30 11:32:41
# Project: common
from six.moves.urllib.parse import urlparse
import time

from pyspider.libs.base_handler import every, config
from pyspider.libs.url import _build_url

from handler.udb_handler import UDBHandler
from atlproc import newspaperEngine



class CommonSiteHandler(UDBHandler):
    crawl_config = {
        'headers': {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        }
    }

    UPDATE_SETTINGS_INTERVAL = 60
    UPDATE_KEYWORDS_INTERVAL = 60
    UPDATE_PROXIES_INTERVAL = 60*12

    SETTING_TYPE = 'common'
    
    parser = newspaperEngine()

    def get_settings(self):
        return self.api.get_common_settings()

    def generate_urls(self):
        return self.settings.keys()

    def crawl(self, url, **kwargs):
        # 1. 直接使用初始入口配置，当配置更新后 正在抓取的所有url以及由这些url产生的子url还会使用旧的配置。
        # if kwargs.get('save', {}).get('proxy_on', False):
        #     kwargs['proxy'] = self.proxy_manager.pick_one()

        # 2.直接使用url, 由此url为入口的所有url都使用一个配置，判断消耗少
        save = dict(kwargs.get('save', {}))
        base_url = save.get('base_url', None)
        if base_url:
            if self.settings.get(base_url, {}).get('proxy_on', False):
                kwargs['proxy'] = self.proxy_manager.pick_one()
            if self.settings.get(base_url, {}).get('js_on', False):
                kwargs['fetch_type'] = 'js'

            cur_depth = save.get('cur_depth', None)
            if cur_depth is None:
                save['cur_depth'] = self.settings.get(url, {}).get('max_depth', 2)
            else:
                save['cur_depth'] = cur_depth - 1

            kwargs['save'] = save

        # 3.使用域名做key，保证此域名都使用一个配置，但是每次爬取判断消耗的资源更多

        return super(CommonSiteHandler, self).crawl(url, **kwargs)

    @every(minutes=1)
    def on_start(self):
        self.check_update()
        urls = self.generate_urls()
        for url in urls:
            context = {
                'base_url': url,
                # 'proxy_on': self.settings[parsed.hostname]['proxy_on'],
                # 'hostname': urlparse(url).hostname,
            }
            self.crawl(url, callback=self.index_page, save=context, force_update=True)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        cur_depth = response.save.get('cur_depth', 0)
        if cur_depth > 0:
            for each in response.doc('a[href^="http"]').items():
                title = each.text().strip(' \n\r\t')
                if title and any(title.find(kw) > -1 for kw in self.keywords):
                    self.crawl(each.attr.href, callback=self.index_page, save=response.save)
        else:
            return self.parse(response)
            
    def parse(self, response):
        article = self.parser.parse(response.text)
        return {
            "url": response.url,
            'type':'common',
            "html": response.text,
            "title": article.title,
            "text": article.text,
            "authors": '|'.join(article.authors),
            "publish_time": time.mktime(article.publish_date.timetuple()) if article.publish_date else None,
        }