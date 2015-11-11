#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mithril
# @Date:   2015-09-24 10:10:08
# @Last Modified by:   mithril
# @Last Modified time: 2015-10-15 14:45:00

try:
    from urllib import parse as urlparse
except ImportError:
    import urlparse

def connect_database(url):
    parsed = urlparse.urlparse(url)
    engine = parsed.scheme

    if engine == 'mysql':
        pass
    elif engine == 'sqlite':
        pass
    elif engine == 'mongodb':
        from .mongodb import SpiderSettingDB
        return SpiderSettingDB(url)
    elif engine == 'sqlalchemy':
        pass
    else:
        raise Exception('unknown engine: %s' % engine)
