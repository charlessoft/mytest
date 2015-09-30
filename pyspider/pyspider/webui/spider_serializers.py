#!/usr/bin/env python
# -*- encoding: utf-8 -*-

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
    proxy_on = colander.SchemaNode(colander.Boolean(), missing=False)
    js_on = colander.SchemaNode(colander.Boolean(), missing=False)
    max_depth = colander.SchemaNode(colander.Integer(), validator=colander.Range(0, 20), missing=2)


class Settings(colander.SequenceSchema):
    setting = Setting()


class Keywords(colander.SequenceSchema):
    keyword = colander.SchemaNode(colander.String())


class Accounts(colander.SequenceSchema):
    account = colander.SchemaNode(colander.String())


class Proxies(colander.SequenceSchema):
    proxy = colander.SchemaNode(colander.String())
