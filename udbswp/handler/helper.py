#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mithril
# @Date:   2015-09-24 10:10:08
# @Last Modified by:   mithril
# @Last Modified time: 2015-10-15 14:46:02


# helper method for handler

from pyspider.libs.utils import ObjectDict


def get_setting_by_domain(domain):
    return {}



class ProxyManager(object):
    def __init__(self, proxies=[]):
        self.replace(proxies)

    def replace(self, proxies):
        if not proxies:
            proxies = []
        self.proxies = list(proxies)
        self.record = {}
        self._cur = 0
        self._total = len(self.proxies)

    def pick_one(self):

        proxy = self.proxies[self._cur] if self._total > 0 else None

        if self._cur < self._total - 1:
            self._cur += 1
        else:
            self._cur = 0

        return proxy


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
        if isinstance(result, (list, tuple)):
            for r in result:
                super(ListResultMixin, self).on_result(r)
        else:
            super(ListResultMixin, self).on_result(result)
