# -*- coding: UTF-8 -*-
__author__ = 'chenqian'
from pyv8 import PyV8


class v8Cookie(PyV8.JSClass):
    def match(self, js_content):
        pass


class v8Navigator(PyV8.JSClass):
    @property
    def appName(self):
        return "Netscape"


class v8HtmlScriptElement(PyV8.JSClass):
    # @property
    # def src(self):
    # pass

    @property
    def onreadystatechange(self):
        pass

        # def appendChild(self,element):
        # pass


class v8Doc(PyV8.JSClass):
    def write(self, s):
        print s.decode('utf-8')

    def __init__(self):
        self.m_cookie = v8Cookie()

        # @property
        # def src(self):
        # pass

    @property
    def onload(self):
        pass

    def createElement(self, element):
        return v8HtmlScriptElement()

    def getElementsByTagName(self, element):
        return v8HtmlScriptElement()

    @property
    def cookie(self):
        logging.info("cookie--init!!")
        return self.m_cookies.match("ss")
        # if self.m_cookies == None:
        # self.m_cookies = v8Cookie()
        # return self.m_cookies

    def match(self, js):
        pass


class v8Win(PyV8.JSClass):
    def hello(self, s):
        print s.decode('utf-8')

    @property
    def navigator(self):
        return v8Navigator()

    @property
    def onreadystatechange(self):
        pass

        # @property
        # def onload(self):
        # return

    def setTimeout(self, func, timeinter):
        pass


class Global(PyV8.JSClass):
    def __init__(self):
        self.document = v8Doc()
        self.window = v8Win()
