#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mithril
# @Date:   2015-09-21 10:18:04
# @Last Modified by:   mithril
# @Last Modified time: 2015-10-15 14:41:39


import colander

def url_validator(node, url):
    if not (url.find('http://') == 0 or url.find('https://') == 0):
        raise colander.Invalid(node, '%s missing schema' % url)

class Article(colander.MappingSchema):
    url = colander.SchemaNode(colander.String())
    title = colander.SchemaNode(colander.String())
    text = colander.SchemaNode(colander.String())
    authors = colander.SchemaNode(colander.String())
    publish_time = colander.SchemaNode(colander.String())
    keywords = colander.SchemaNode(colander.String())
    tags = colander.SchemaNode(colander.String())
    updatetime = colander.SchemaNode(colander.Float())


class Articles(colander.SequenceSchema):
    article = Article()


class Setting(colander.MappingSchema):
    url = colander.SchemaNode(colander.String(), validator=url_validator)
    name = colander.SchemaNode(colander.String(), missing='')
    proxy_on = colander.SchemaNode(colander.Boolean(), missing=False)
    js_on = colander.SchemaNode(colander.Boolean(), missing=False)
    max_depth = colander.SchemaNode(colander.Integer(), validator=colander.Range(0, 20), missing=2)
    extra = colander.SchemaNode(colander.String(), missing='')


class Settings(colander.SequenceSchema):
    setting = Setting()


class Keywords(colander.SequenceSchema):
    keyword = colander.SchemaNode(colander.String())


class Accounts(colander.SequenceSchema):
    account = colander.SchemaNode(colander.String())


class Proxies(colander.SequenceSchema):
    proxy = colander.SchemaNode(colander.String())
