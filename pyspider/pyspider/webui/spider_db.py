#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import time


class SpiderBaseDB(object):
    __database_name__ = 'spider'
    __collection_name__ = None

    def __init__(self, conn):
        if not self.__collection_name__:
            raise Exception('must define __collection_name__')

        self.collection = conn[self.__database_name__][self.__collection_name__]

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

    def save(self, query, obj):
        obj['updatetime'] = time.time()
        return self.collection.update(
            query, {"$set": obj}, upsert=True
        )


class SpiderArticleDB(SpiderBaseDB):
    __collection_name__ = 'article'


class SpiderSettingDB(SpiderBaseDB):
    __collection_name__ = 'setting'



