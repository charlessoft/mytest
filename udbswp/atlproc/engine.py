#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mithril
# @Date:   2015-09-24 10:10:08
# @Last Modified by:   mithril
# @Last Modified time: 2015-10-15 14:45:40


from newspaper import Article

from goose import Goose
from goose.text import StopWordsChinese

class newspaperEngine(object):
    def __init__(self):
        pass

    def parse(self, content):
        article = Article('', language='zh', memoize_articles=False, fetch_images=False)
        article.download(html=content)
        article.parse()
        return article

class gooseEngine(object):
    def __init__(self):
        self.g = Goose({'stopwords_class': StopWordsChinese})

    def parse(self, content):
        article = self.g.extract(raw_html=content)
        article.text = article.cleaned_text
        return article