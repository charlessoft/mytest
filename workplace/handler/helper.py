#coding=utf-8

# helper method for handler

from pyspider.libs.base_handler import *
from pyspider.libs.utils import ObjectDict


def get_proxy_list():
    proxy_list = []
    return proxy_list

def get_keywords():
    keywords = [u'电力', u'电网|尼玛']
    return keywords

def get_settings(tp):
    if tp == 'search':
        return []
    elif tp == 'people':
        return []
    else:
        tp == 'common'
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

        settings = {}

        for url in target_urls:
            settings[url] = {}
            settings[url]['proxy_on'] = False
            settings[url]['need_parse'] = False
            settings[url]['max_recurrence'] = 2


def get_setting_by_domain(domain):
    return {}


class ProxyManager(object):
    def __init__(self, proxies=[]):
        self.update(proxies)

    def update(self, proxies):
        self.proxies = list(proxies)
        self.record = {}
        self._cur = 0
        self._total = len(self.proxies)

    def pick_one(self):

        proxy = self.proxies[self._cur] if self._total > 0 else None
                
        if self._cur < self._total -1 :
            self._cur +=1
        else:
            self._cur = 0
        
        return proxy


# get keywords here

keywords = ['电力']


def keywords_in(txt, keywords):
    txt = txt.strip(' \n\r\t')
    if txt and any(txt.find(kw) > -1 for kw in keywords):
        return True

def keywords_in_result(result):
    return keywords_in(result.get('title', '') + result.get('text', ''))

def filter_keywords(func):
    def wrap():
        results = func()
        if hasattr(results, '__iter__'):
            results = filter(keywords_in_result, results)
        else:
            if not keywords_in_result(results):
                results = None
        return results

    return wrap


class ListResultMixin(object):
    def on_result(self, result):
        """Receiving returns from other callback, override me."""
        if not result:
            return
        assert self.task, "on_result can't outside a callback."
        if self.is_debugger():
            pprint(result)
        
        if self.__env__.get('result_queue'):
            for r in result:
                self.__env__['result_queue'].put((self.task, result))