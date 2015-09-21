__author__ = 'charles'

# from pyspider.libs.base_handler import *
# from urllib import quote
# from weibo.login import WeiboLogin, WeiboLoginFailure
import urllib
import sys
import requests
# from pyspider.libs.base_handler import *

username = 'chenqian'
password = 'a123456789'


class YRLogin(object):
    def __init__(self):
        self.m_oa_config = {
            'oa_login_url': 'http://oa.yirong-info.com:8000/names.nsf?Login',

        }
        self.m_session = requests.session()
        self.m_username = username
        self.m_password = password
        self.m_login_data = {
            '%25%25ModDate': '0000000000000000',
            'Path': '%2Fdomcfg.nsf%2Fimages%2F%24file',
            'Username': '',
            'Password': '',
            '%25%25Surrogate_AutoSave': '1',
            'AutoSave': '1',
            'RedirectTo': '%2F',
            'ReasonText': '',
            '%24PublicAccess': '1',
            'reasonType': '0',
            'SaveOptions': '0',
            'Remote_Addr': '10.142.51.22',
        }

        pass

    def set_userinfo(self, username, password):
        self.m_username = username
        self.m_password = password
        self.m_login_data['Username'] = username
        self.m_login_data['Password'] = password

    def login(self):
        print self.m_login_data
        self.m_login_data = urllib.urlencode(self.m_login_data)
        headers = {}
        cookies = {}
        cookies['Cookie'] = 'LastLoginUser=%s' % self.m_username
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Origin'] = 'http://oa.yirong-info.com:8000'
        headers['Upgrade-Insecure-Requests'] = 1
        headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Referer'] = 'http://oa.yirong-info.com:8000/'
        print self.m_login_data

        self.m_session.post(self.m_oa_config['oa_login_url'], data=self.m_login_data, headers=headers, cookies=cookies)
        print self.m_session.cookies
        return self.m_session
        # print self.m_session.status_code
        # print self.m_session.text
        # print self.m_session.cookies


if __name__ == '__main__':
    yr_oa = YRLogin()
    yr_oa.set_userinfo(username, password)
    yr_oa.login()
