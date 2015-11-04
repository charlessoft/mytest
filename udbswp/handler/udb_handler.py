#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mithril
# @Date:   2015-09-24 10:10:08
# @Last Modified by:   mithril
# @Last Modified time: 2015-10-15 14:46:07


from pyspider.libs.base_handler import BaseHandler
from pyspider.libs.utils import md5string
from udbswp.handler.helper import ProxyManager
from udbswp.handler.api import Api
from udbswp import config
from pprint import pprint
import time
import ujson
import dateutil.parser


ENABLE_JSON_RESULT = getattr(config, 'ENABLE_JSON_RESULT', False)
UDB_RESULT_QUEUE_NAME = getattr(config, 'UDB_RESULT_QUEUE_NAME', 'udb_result')


class UDBHandler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        }
    }

    RESULT_FIELDS = ['url', 'type', 'title', 'text', 'authors', 'publish_time', 'keywords']

    UPDATE_SETTINGS_INTERVAL = 3600
    UPDATE_KEYWORDS_INTERVAL = 3600
    UPDATE_PROXIES_INTERVAL = 3600*12

    SETTING_TYPE = 'common'
    KEYWORD_TYPE = 'common'

    def __init__(self):
        self.api = Api()
        self.update_settings()
        self.update_keywords()
        self.update_proxies()

    def check_update(self):
        if time.time() - self.last_update_settings > self.UPDATE_SETTINGS_INTERVAL:
            self.update_settings()
        if time.time() - self.last_update_keywords > self.UPDATE_KEYWORDS_INTERVAL:
            self.update_settings()
        if time.time() - self.last_update_proxies > self.UPDATE_PROXIES_INTERVAL:
            self.update_settings()

    def get_settings(self):
        return self.api.get_settings(self.SETTING_TYPE)

    def get_keywords(self):
        return self.api.get_keywords(self.KEYWORD_TYPE)

    def get_proxies(self):
        return self.api.get_proxies()

    def update_settings(self):
        self.settings = self.get_settings()
        self.last_update_settings = time.time()

    def update_keywords(self):
        self.keywords = self.get_keywords()
        self.last_update_keywords = time.time()

    def update_proxies(self):
        self.proxies = self.api.get_proxies()
        self.proxy_manager = ProxyManager(self.proxies)
        self.last_update_proxies = time.time()

    def pick_proxy(self):
        return self.proxy_manager.pick_one()

    # def crawl(self, url, **kwargs):
    #     if self.settings.get('proxy_on', False):
    #         kwargs['proxy'] = self.proxy_manager.pick_one()
    #     if self.settings.get('js_on', False):
    #         kwargs['fetch_type'] = 'js'

    #     return self.crawl(url, **kwargs)

    # def get_taskid(self, task):
    #     '''Generate taskid by information of task md5(url) by default, override me'''
    #     return md5string(task['url'])

    def clean_result(self, result):
        """ keep result in certain format """
        # for k in result.keys():
        #     if k not in self.RESULT_FIELDS:
        #         del result[k]

        if 'publish_time' in result:
            if result['publish_time']:
                try:
                    result['publish_time'] = int(result['publish_time'])
                except:
                    publish_date = dateutil.parser.parse(result['publish_time'])
                    result['publish_time'] = int(time.mktime(publish_date))
            else:
                result['publish_time'] = 0

        result['update_time'] = int(time.time())

        return result

    def on_result(self, result):
        """Receiving returns from other callback, override me."""
        if not result:
            return
        assert self.task, "on_result can't outside a callback."
        if self.is_debugger():
            pprint(result)

        result_queue = self.__env__.get('result_queue')

        if result_queue:
            cleaned_result = self.clean_result(result)
            if cleaned_result.get('url', self.task['url']) != self.task['url']:
                new_task = self.task.copy()
                new_task['url'] = cleaned_result['url']
                new_task['taskid'] = self.get_taskid(new_task)
                result_queue.put((new_task, cleaned_result))
            else:
                result_queue.put((self.task, cleaned_result))

            # pack obj by ujson
            if ENABLE_JSON_RESULT and hasattr(result_queue, 'redis'):
                result_queue.redis.rpush(UDB_RESULT_QUEUE_NAME, ujson.dumps(cleaned_result))




class UDBListResultHandler(UDBHandler):

    def on_result(self, result):
        if not result:
            return
        assert self.task, "on_result can't outside a callback."
        if self.is_debugger():
            pprint(result)

        if self.__env__.get('result_queue'):
            for r in result:
                self.__env__['result_queue'].put((self.task, self.clean_result(result)))


class UDBCommonHandler(UDBHandler):
    def on_result(self, result):
        """Receiving returns from other callback, override me."""
        if not result:
            return
        assert self.task, "on_result can't outside a callback."
        if self.is_debugger():
            pprint(result)

        if self.__env__.get('result_queue'):
            if isinstance(result, (list, tuple)):
                for r in result:
                    self.__env__['result_queue'].put((self.task, self.clean_result(r)))
            else:
                self.__env__['result_queue'].put((self.task, self.clean_result(result)))