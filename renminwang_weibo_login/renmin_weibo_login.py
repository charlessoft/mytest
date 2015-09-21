# -*- coding: UTF-8 -*-
import time
import requests
import urllib
import sys
import re
import xml.dom.minidom
import string
import random
#import socket
#import socks
reload(sys)
sys.setdefaultencoding('utf-8')

username = 'studio20130101'
password = 'aA123456789'

class renmin_login():
    def __init__(self):
        self.m_session = requests.session()
        pass


    def forwardIndex_action(self):
        self.m_func = '[forwardIndex_action]\n'
        self.m_url = 'http://t.people.com.cn/forwardIndex.action'
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
        headers["Referer"] = "http://t.people.com.cn/"
        headers['Upgrade-Insecure-Requests']='1'
        self.m_session.headers.update(headers)
        self.m_session.get(self.m_url,headers=headers)
        print self.m_func
        print self.m_session.cookies
        print self.m_session.headers

    def userAccessLog_action(self):
        self.m_func = '[userAccessLog_action]\n'
        print self.m_func
        # print self.m_session.headers
        #self.m_url = 'http://t.people.com.cn/userAccessLog.action'
        self.m_url = 'http://t.people.com.cn/userAccessLog.action'
        r = self.m_session.get(self.m_url)
        #print self.m_session.cookies
        #print r.headers
        print r.text

    def login_action(self):
        self.m_func = '[login_action]'
        self.m_url = 'http://t.people.com.cn/login.action'
        login_data = {
            'userName':username,
            'password': password ,
            'isremember':'true',
            '__checkbox_isremember':'true'
        }
        r = self.m_session.post(self.m_url,data=login_data)
        print r.history[0].headers
        # print r.cookies
        return self.m_session



if __name__ == '__main__':
    renmin = renmin_login()
    renmin.forwardIndex_action()
    renmin.userAccessLog_action()
    renmin.login_action()
    pass
