#!/usr/bin/env python
# -*- encoding: utf-8 -*-

class BaseDB(object):

    def get_settings(self, name):
        raise NotImplementedError

    def set_settings(self, name, value):
        raise NotImplementedError

    def get_keywords(self, name):
        raise NotImplementedError

    def set_keywords(self, name, value):
        raise NotImplementedError

    def get_accounts(self, tp):
        raise NotImplementedError

    def set_accounts(self, tp, value):
        raise NotImplementedError

    def get_proxies(self):
        raise NotImplementedError

    def set_proxies(self, value):
        raise NotImplementedError
