#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import colander


class Article(colander.MappingSchema):
    url = colander.SchemaNode(colander.String())
    title = colander.SchemaNode(colander.String())
    text = colander.SchemaNode(colander.String())
    authors = colander.SchemaNode(colander.String())
    publish_date = colander.SchemaNode(colander.String())
    keywords = colander.SchemaNode(colander.String())
    tags = colander.SchemaNode(colander.String())
    updatetime = colander.SchemaNode(colander.Float())


class Articles(colander.SequenceSchema):
    article = Article()

class Setting(colander.MappingSchema):
    domain = colander.SchemaNode(colander.String())
    proxy_on = colander.SchemaNode(colander.Boolean())
    js_on = colander.SchemaNode(colander.Boolean())
    max_recurrence = colander.SchemaNode(colander.Integer(), validator=colander.Range(0, 20))
    updatetime = colander.SchemaNode(colander.Float())

class Settings(colander.SequenceSchema):
    setting = Setting()