#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import request
from flask.ext.restful import reqparse, abort, Resource, fields, marshal_with
from bson.son import SON
from pymongo import ASCENDING, DESCENDING
import time
import json

from spider_serializers import Setting, Settings

from .app import app, api

setting_parser = reqparse.RequestParser()
setting_parser.add_argument('domain', location='args', required=True)
setting_parser.add_argument('proxy_on', location='args', type=bool, default=False)
setting_parser.add_argument('js_on', location='args', type=bool, default=False)
setting_parser.add_argument('max_recurrence', location='args', type=int, default=3)

setting_fields = {
    'domain': fields.String,
    'proxy_on': fields.Boolean,
    'js_on': fields.Boolean,
    'max_recurrence': fields.Integer,
    'updatetime': fields.Float,
}

class SpiderSettingBase(Resource):
    __database_name__ = 'spider'
    __collection_name__ = 'setting'

    @property
    def collection(self):
        if hasattr(self, '_collection'):
            return getattr(self, '_collection')

        resultdb = app.config['resultdb']
        _collection = resultdb.conn[self.__database_name__][self.__collection_name__]
        setattr(self, '_collection', _collection)
        return _collection


@api.resource('/spider/setting')
class SpiderSetting(SpiderSettingBase):

    @marshal_with(setting_fields)
    def get(self):
        args = setting_parser.parse_args()
        result = self.collection.find_one({'domain': args['domain']})
        return result, 200 if result else 404

    def put(self):
        deserialized = Setting().deserialize(json.loads(request.data))
        obj = {
            'domain':deserialized['domain'],
            'proxy_on':deserialized['proxy_on'],
            'js_on':deserialized['js_on'],
            'max_recurrence':deserialized['max_recurrence'],
            'updatetime': time.time(),
        }

        try:
            self.collection.update({'domain':deserialized['domain']}, {"$set": obj}, upsert=True)
        except Exception as e:
            return {'error_msg': repr(e)}, 500
        else:
            return {}

    def delete(self):
        args = setting_parser.parse_args()
        result = self.collection.remove({'domain': args['domain']})
        return {}

@api.resource('/spider/setting/list')
class SpiderSettingList(SpiderSettingBase):

    @marshal_with(setting_fields)
    def get(self):
        return tuple(self.collection.find())

    def put(self):
        deserialized = Settings().deserialize(json.loads(request.data))
        try:
            for obj in deserialized:
                self.collection.update({'domain': obj['domain']}, {"$set": obj}, upsert=True)
        except Exception as e:
            return {'error_msg': repr(e)}, 500
        else:
            return {}

    def delete(self):
        domain_list = json.loads(request.data)
        if not isinstance(domain_list, list):
            return {'error_msg': 'domain_list is not valid'}, 500

        try:
            for domain in domain_list:
                self.collection.remove({'domain': domain})
        except Exception as e:
            return {'error_msg': repr(e)}, 500
        else:
            return {}
