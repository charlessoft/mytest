#!/usr/bin/env python
# -*- encoding: utf-8 -*-


from pyspider.libs.base_handler import BaseHandler
from six
from pprint import pprint
import time


class UDBHandler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        }
    }


    RESULT_FIELDS = ['url', 'html', 'title', 'text', 'authors', 'publish_date']

    def __init__(self):
        self.last_update_settings = time.time()


    # def get_taskid(self, task):
    #     '''Generate taskid by information of task md5(url) by default, override me'''
    #     return md5string(task['url'])


    def on_result(self, result):
        """Receiving returns from other callback, override me."""
        if not result:
            return
        assert self.task, "on_result can't outside a callback."
        if self.is_debugger():
            pprint(result)

        # keep fields format

        for k in result.keys():
            if k not in self.RESULT_FIELDS:
                del result[k]

        if 'publish_date' in result:
            pass

        if self.__env__.get('result_queue'):
            self.__env__['result_queue'].put((self.task, result))