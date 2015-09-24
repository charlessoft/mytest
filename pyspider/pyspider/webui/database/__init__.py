#!/usr/bin/env python
# -*- encoding: utf-8 -*-

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
