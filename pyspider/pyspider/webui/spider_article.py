#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mithril
# @Date:   2015-09-21 10:18:04
# @Last Modified by:   mithril
# @Last Modified time: 2015-10-19 15:29:47



from flask.ext.restful import reqparse, abort, Resource, fields, marshal_with
from bson.son import SON
from pymongo import ASCENDING, DESCENDING
import time

import logging
logger = logging.getLogger('webui')

from .app import app, api


parser = reqparse.RequestParser()
parser.add_argument('keywords', action='append', help='document keyword list')
parser.add_argument('tags', action='append')
parser.add_argument('offset', type=int)
parser.add_argument('limit', type=int)
parser.add_argument('time_start', type=int, required=True)
parser.add_argument('time_end', type=int, required=True)

article_fields = {
    'url': fields.String,
    "title": fields.String,
    "text": fields.String,
    "authors": fields.String,
    "publish_time": fields.String,
    'keywords': fields.String,
    'tags': fields.String,
    'updatetime': fields.Float,
}


class SpiderArticleBase(Resource):
    __database_name__ = 'spider'
    __collection_name__ = 'article'

    @property
    def collection(self):
        if hasattr(self, '_collection'):
            return getattr(self, '_collection')

        resultdb = app.config['resultdb']
        _collection = resultdb.conn[self.__database_name__][self.__collection_name__]
        setattr(self, '_collection', _collection)
        return _collection


@api.resource('/spider/article')
class SpiderArticle(SpiderArticleBase):

    @marshal_with(article_fields)
    def get(self):
        args = parser.parse_args()
        keywords = args['keywords']
        tags = args['tags']
        offset = args['offset']
        limit = args['limit']
        time_start = args['time_start']
        time_end = args['time_end']

        pipeline = []
        match = {}
        match_or = []
        match_and = []

        match['updatetime'] = {'$gte': time_start, '$lte': time_end}

        if keywords:
            match_or.append({'keywords':{'$in': keywords }})
        if tags:
            match_or.append({'tags':{'$in': tags }})

        if len(match_or) :
            match['$or'] = match_or

        if len(match_and) :
            match['$and'] = match_and

        pipeline.append({'$match':match})

        if offset:
            pipeline.append({'$offset': offset})
        if limit:
            pipeline.append({'$limit': limit})

        # logger.debug('construct aggregate pipeline: %s' % pipeline)

        return self.collection.aggregate(pipeline).get('result')

