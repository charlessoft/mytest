#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import requests
import logging

from pyspider.webui.database.const import AccountTypeName, KeywordTypeName, SettingTypeName
from pyspider.webui.database import connect_database

from udbswp import config

logger = logging.getLogger('spider_api')

API_BASE_URL = getattr(config, 'API_BASE_URL', 'http://localhost:5000/')
PROXY_API_URL = API_BASE_URL + 'spider/proxies'
KEYWORD_API_URL = API_BASE_URL + 'spider/keywords/'
SETTING_API_URL = API_BASE_URL + 'spider/settings/'
ACCOUNT_API_URL = API_BASE_URL + 'spider/accounts/'

API_DB_URL = getattr(config, 'API_DB_URL', 'mongodb://10.142.49.230:27088/')


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


class SpiderDBApi(object):
    def __init__(self):
        self.db = connect_database(API_DB_URL)

    @result_on_error(default=[])
    def get_proxies(self):
        return self.db.get_proxies()

    @result_on_error(default=[])
    def get_keywords(self, tp=KeywordTypeName.Common):
        keywords = self.db.get_keywords(tp)
        return keywords

    @result_on_error(default={})
    def get_settings(self, tp=SettingTypeName.Common):
        settings = self.db.get_settings(tp)
        return settings

    @result_on_error(default={})
    def get_accounts(self, tp):
        accounts = self.db.get_accounts(tp)
        return accounts

    @result_on_error(default={})
    def get_common_settings(self):
        list_settings = self.db.get_settings(SettingTypeName.Common)
        dict_settings = {}
        for item in list_settings:
            url = item['url']
            del item['url']
            dict_settings[url] = item

        return dict_settings

class SpiderApi(object):
    def _api_get(self, url, params=None):
        params = params or {}
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        result = r.json()
        return result

    @result_on_error(default=[])
    def get_proxies(self):
        proxies = self._api_get(PROXY_API_URL)
        return proxies

    @result_on_error(default=[])
    def get_keywords(self, tp=KeywordTypeName.Common):
        keywords = self._api_get(KEYWORD_API_URL, tp)
        return keywords

    @result_on_error(default={})
    def get_settings(self, tp=SettingTypeName.Common):
        settings = self._api_get(SETTING_API_URL + tp)
        return settings

    @result_on_error(default={})
    def get_accounts(self, tp):
        accounts = self._api_get(ACCOUNT_API_URL + tp)
        return accounts

    @result_on_error(default={})
    def get_common_settings(self):
        list_settings = self._api_get(SETTING_API_URL + SettingTypeName.Common)
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

    def get_settings(self, tp=None):
        settings = {
            'proxy_on': False,
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


Api = SpiderDBApi

if __name__ == '__main__':
    api = Api()
    settings = api.get_common_settings()
    print settings
