#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import requests
import logging

logger = logging.getLogger('spider_api')

PROXY_API_URL = ''
KEYWORD_API_URL = ''
SETTING_API_URL = ''
ACCOUNT_API_URL = ''
COMMON_SETTING_API_URL = ''


def result_on_error(default=None):
    def wrap(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                result = default
            return result
        return wrapper
    return wrap


class SpiderApi(object):

    def _api_get(self, url, params):
        params = params or {}
        r = requests.get(url, params=params)
        r.raise_for_status()
        result = r.json()
        return result

    @result_on_error(default=[])
    def get_proxies(self):
        proxies = self._api_get(PROXY_API_URL)
        return proxies

    @result_on_error(default=[])
    def get_keywords(self):
        keywords = self._api_get(KEYWORD_API_URL)
        return keywords

    @result_on_error(default={})
    def get_settings(self, tp=None):
        settings = self._api_get(SETTING_API_URL, params={'type': tp})
        return settings

    @result_on_error(default={})
    def get_accounts(self, tp=None):
        accounts = self._api_get(ACCOUNT_API_URL, params={'type': tp})
        return accounts

    @result_on_error(default={})
    def get_common_settings(self):
        list_settings = self._api_get(COMMON_SETTING_API_URL)
        dict_settings = {}
        for item in list_settings:
            url = item['url']
            del item['url']
            dict_settings[url] = item

        return dict_settings


class FakeSpiderApi(object):

    def get_proxies(self):
        proxy_list = []
        return proxy_list

    def get_keywords(self):
        keywords = [u'电力', u'电网|尼玛']
        return keywords

    def get_accounts(self, tp=None):
        accounts = [u'哈哈']
        return accounts

    def get_settings(self,tp=None):
        settings = {
            'proxy_on' : False,
            'js_on': False
        }
        return settings

    def get_common_settings(self):
        dict_settings = {}
        target_urls = [
            'http://www.chem17.com/offer_sale/detail/7156621.html',
            'http://baozoumanhua.com/articles/3744536',
            'http://www.cr-power.com/',
            'http://shaoxing.19lou.com/forum-733-thread-114931414837769942-1-1.html',
            'http://www.shumilou.com/chaojidianliqiangguo/',
            'http://www.zepc.edu.cn/',
            'http://www.tdqs.com/',
            'http://www.nepcc4.com.cn/',
            'http://www.nepco.net.cn/',
            'http://www.ybzhan.cn/Product/detail/6485411.html',
            'http://www.geta.org.cn/',
            'http://www.contron.com.cn/',
        ]

        for url in target_urls:
            dict_settings[url] = {}
            dict_settings[url]['proxy_on'] = False
            dict_settings[url]['need_parse'] = False
            dict_settings[url]['max_depth'] = 2

        return dict_settings


Api = FakeSpiderApi