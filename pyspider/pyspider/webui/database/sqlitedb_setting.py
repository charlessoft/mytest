# -*- coding: UTF-8 -*-
__author__ = 'charles'

from flask import request
from flask.ext.restful import reqparse, abort, Resource, fields, marshal_with

from bson.son import SON
from pymongo import ASCENDING, DESCENDING
import time
import json

from spider_serializers import Setting, Settings

# from .app import app, api
import sqlite3

# from .sqlitebase import SQLiteMixin
# from pyspider.database.base.projectdb import ProjectDB as BaseProjectDB
from pyspider.database.basedb import BaseDB

class sqlitedb_setting(BaseDB):
    placeholder = '?'

    def __init__(self, path=''):
        self.path = path
        self.conn = None
        self.tablename = 'setting'
        self.col_common_setting = 'common_setting'
        self.col_proxies = 'proxies'
        self.col_keywords = 'keywords'
        self.col_bloger = 'bloger'

    @property
    def dbcur(self):
        if not (self.conn):
            self.conn = sqlite3.connect(self.path, isolation_level=None)
        return self.conn.cursor()

    def _get_value(self, keyname):
        where = "`key` = '%s'" % keyname
        for each in self._select2dic(tablename=self.tablename, where=where):
            return each['value']

    def _set_value(self, keyname, jsonsetting):
        obj = {'value': jsonsetting.decode('utf-8')}
        where = "`key` = '%s'" % keyname
        ret = self._update(tablename=self.tablename, where=where, **obj)
        # print ret.rowcount
        return ret

    def get_common_setting(self):
        return self._get_value(self.col_common_setting)

    def set_common_setting(self, value):
        return self._set_value(self.col_common_setting, value)

    def get_proxies(self):
        return self._get_value(self.col_proxies)

    def set_proxies(self, value):
        return self._set_value(self.col_proxies, value)

    def set_keywords(self, value):
        return self._set_value(self.col_keywords, value)

    def get_keywords(self):
        return self._get_value(self.col_keywords)

    def get_bloger(self):
        return self._get_value(self.col_bloger)

    def set_bloger(self, value):
        return self._set_value(self.col_bloger, value)



if __name__ == '__main__':
    sqlite = sqlitedb_setting('/Users/tina/workspace/yr_prj/udb-spider/db/setting.db')
    # args ={ "settings": [ { "url": "www.baidu.com" , "name":"百度","js_on": True, "proxy_on": True,"max_depth": 5 } ]}
    # sqlite.test()
    # args={'a':1,'b':2}
    # sqlite.test({'a':'I', 'b':'am', 'c':'wcdj'})
    # sqlite.test(gerry='gerry@byteofpython.info', wcdj='wcdj@126.com', yj='yj@gmail.com')
    # sqlite.set_value('common_setting','{ "settings": [ { "url": "www.baidu.com" , "name":"百度","js_on": true, "proxy_on": true,"max_depth": 5 } ]}')
    # sqlite.set_value('proxies','{ "proxies": [(10.142.49.128, 8888), (10.142.49.128, 9999)]}')
    # sqlite.setsetting("{'a':'I', 'b':'am', 'c':'wcdj'}")
    # sqlite.exist_keyname('common_setting')

    # print sqlite.get_value('common_setting')
    print sqlite.get_bloger();
    print sqlite.get_keywords()
    print sqlite.get_common_setting()
    print sqlite.get_proxies()



# 'id':int,               # id
# 'name': str,            # 名称
# 'url':str,              # url
# 'type':str,             # 类型（一般站点可能无用）
# 'js_on': bool,          # 启用js
# 'proxy_on': bool,       # 启用代理
# 'max_depth': int,  		# 最大深度

