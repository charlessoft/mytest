#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mithril
# @Date:   2015-09-24 10:10:08
# @Last Modified by:   mithril
# @Last Modified time: 2015-10-15 14:45:03


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
