#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mithril
# @Date:   2015-09-24 10:10:08
# @Last Modified by:   mithril
# @Last Modified time: 2015-10-15 14:45:07


import time
from pymongo import MongoClient
from .const import AccountTypeName, KeywordTypeName, SettingTypeName
from .base import BaseDB


class SpiderBaseCollection(object):
    COLLECTION = None

    def __init__(self, db):
        if not self.COLLECTION:
            raise Exception('must define COLLECTION')

        self.collection = db[self.COLLECTION]
        self.collection.ensure_index('name', unique=True)

    def get(self, key):
        item = self.collection.find_one({}, {key: 1})
        return item.get(key, None) if item else None

    def set(self, key, value):
        obj = dict({
            key: value,
            'updatetime': time.time()
        })
        return self.collection.update(
            {}, {"$set": obj}, upsert=True
        )

    # def get(self, key):
    #     item = self.collection.find_one({key: { '$exists': True }}, {key: 1})
    #     return item.get(key, None) if item else None

    # def set(self, key, value):
    #     obj = {key: value}
    #     obj['updatetime'] = time.time()
    #     return self.collection.update(
    #         {key: { '$exists': True }}, {"$set": obj}, upsert=True
    #     )

    def save(self, query, obj):
        obj['updatetime'] = time.time()
        return self.collection.update(
            query, {"$set": obj}, upsert=True
        )

    def save_bulk(self, query_key, obj_list):
        bulk = self.collection.initialize_unordered_bulk_op()
        updatetime = time.time()
        for obj in obj_list:
            obj['updatetime'] = updatetime
            bulk.find({query_key: obj[query_key]}).upsert().update_one({
                '$set': obj
            })
        details = bulk.execute()
        return details


class SpiderSettingColletion(SpiderBaseCollection):
    COLLECTION = 'setting'


class SpiderKeywordCollection(SpiderBaseCollection):
    COLLECTION = 'keyword'


class SpiderProxyCollection(SpiderBaseCollection):
    COLLECTION = 'proxy'

    def get(self):
        return super(SpiderProxyCollection, self).get('proxy')

    def set(self, value):
        return super(SpiderProxyCollection, self).set('proxy', value)


class SpiderAccountCollection(SpiderBaseCollection):
    COLLECTION = 'account'


class SpiderSettingDB(BaseDB):
    DATABASE = 'spider'

    def __init__(self, url, database='spider'):
        self.conn = MongoClient(url)
        self.database = self.conn[database]

        self.setting = SpiderSettingColletion(self.database)
        self.keyword = SpiderKeywordCollection(self.database)
        self.proxy = SpiderProxyCollection(self.database)
        self.account = SpiderAccountCollection(self.database)

    def get_settings(self, name):
        return self.setting.get(name)

    def set_settings(self, name, value):
        return self.setting.set(name, value)

    def get_keywords(self, name):
        return self.keyword.get(name)

    def set_keywords(self, name, value):
        return self.keyword.set(name, value)

    def get_accounts(self, tp):
        return self.account.get(tp)

    def set_accounts(self, tp, value):
        return self.account.set(tp, value)

    def get_proxies(self):
        return self.proxy.get()

    def set_proxies(self, value):
        return self.proxy.set(value)

    def get_common_keywords(self):
        return self.setting.get(KeywordTypeName.Common)

    def set_common_keywords(self, value):
        return self.setting.set(KeywordTypeName.Common, value)

    def get_common_settings(self):
        return self.setting.get(SettingTypeName.Common)

    def set_common_settings(self, value):
        return self.setting.set(SettingTypeName.Common, value)
