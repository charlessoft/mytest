# -*- coding: UTF-8 -*-
import time
import requests
import urllib
import sys
reload(sys)
import re
import chardet
import logging

from jsEngine import *

logging.basicConfig( \
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='myapp.log',
    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

from pyquery import PyQuery as pq

sys.setdefaultencoding('utf-8')
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

glob = Global()



class weibo_login():
    def set_userinfo(self, username, password):
        self.m_usernmae = username
        self.m_password = password

    def __init__(self):
        logging.info("init")
        self.m_proxies = {
            # 'http': '192.168.70.96:8888',
            # 'https': '192.168.70.96:8888',
        }
        self.m_usernmae = ''
        self.m_password = ''
        self.m_headers = {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
                }
        self.m_wbilang_10000 = ''
        self.m_cookies = {}
        self.m_xlogin_url = ''
        self.m_env = None
        self.m_c_login_2_url = ''
        self.m_ptui_ver_js_url = ''
        self.m_s = requests.session()
        self.m_s.headers.update(self.m_headers)
        self.m_s.proxies = self.m_proxies
        self.m_regmaster = ''
        self.m_pt_tea = '1'
        self.m_pt_vcode = ''
        self.m_uin = ''
        self.m_appid = ''
        self.m_js_ver = ''
        self.m_js_type = '1'
        self.m_js_ver = '10315'
        self.m_login_sig = ''
        self.m_s_url = ''
        self.m_ptvfsession = ''

        # ptui_checkVC('0','!WSW','\x00\x00\x00\x00\x00\x75\x0f\x05','3f26e7e2ea8c2020dd292499093fcca4cac06c2a7393a3b744993bb1a9e8f1894da5205e8316829d94b3713669ac293f8abd527a432fa5b8','0');
        self.m_check_ret = ''  # ptui_checkVC第1位参数
        self.m_cap_cd = ''  # ptui_checkVC 第2位参数 验证码
        self.m_salt = ''  # check ptui_checkVC 第3位参数
        self.m_pt_verifysession = ''  # ptui_checkVC 第4位参数
        self.m_isRandSale = ''  # ptui_checkVC 最后5位参数
        self.m_check_sig_url = ''


    def dump_c(self, cookies):
        strtmp = ''
        for key, value in cookies.items():
            strtmp = strtmp + '%s=%s;' % (key, value)
        return strtmp

    def jsparse_path(self, jspath):
        jscontent = open(jspath, 'rb').read()
        self.jsparse(jscontent)

    def jsparse(self, js):
        ctxt = PyV8.JSContext(glob)
        ctxt.enter()
        ctxt.eval(js)
        self.m_env = ctxt.locals
        pass



    def t_qq_login_page(self):
        ''' 访问登陆首页,获取iframe_login页面url '''
        self.m_url = 'http://t.qq.com/login.php'
        self.m_func = '[t_qq_login_page]'
        headers = {}
        cookies = {}
        headers.update(self.m_headers)
        r = self.m_s.get(self.m_url, headers=headers, proxies=self.m_proxies, verify=False)
        if r.status_code == requests.codes.ok:
            pattent = r'var url = "(.*)"'
            mt = re.search(pattent, r.content)
            if mt:
                logging.info('===%s ok===' % self.m_func)
                self.m_xlogin_url = mt.groups()[0]
                logging.debug('xlogin_url: %s\n' % self.m_func)
                return True
            else:
                logging.error('no search')
                return False

    def xlogin_iframe(self):
        ''' 获取cookie和js相关变量 '''

        self.m_url = self.m_xlogin_url
        self.m_func = '[xlogin_iframe]'
        # logging.debug(self.m_func)
        headers = {}
        # cookies = {}
        headers.update(self.m_headers)
        headers.update(
                {
                    'Referer':'http://t.qq.com/login.php',
                    'Upgrade-Insecure-Requests':'1'
                    })

        r = self.m_s.get(self.m_url, headers=headers, verify=False)
        encoding = chardet.detect(r.content)['encoding']
        r.encoding = 'utf-8'
        if r.status_code == requests.codes.ok:
            self.m_cookies.update(r.cookies)
            # print '==%s ok==' % self.m_func
            logging.info('===%s ok===' % self.m_func)
            d = pq(r.content)
            pattent = r'loadScript\("(.*?)"'
            mt = re.search(pattent, r.content)
            if mt:
                self.m_c_login_2_url = '%s%s' % ('https://xui.ptlogin2.qq.com', mt.groups()[0].replace("..", ""))

            self.jsparse(str(d("script").text()))
            self.m_ptui_ver_js_url = '%s%s%s%s' % (
                'https://xui.ptlogin2.qq.com', '/ptui_ver.js?v=', self.m_env['Math']['random'](),
                "&ptui_identifier=" + self.m_env.pt.ptui.pt_ver_md5)
            logging.info("ptui_ver_js_url:%s" % self.m_ptui_ver_js_url)

            self.m_regmaster = self.m_env.pt.ptui.regmaster
            self.m_pt_vcode = self.m_env.pt.ptui.pt_vcode_v1
            self.m_appid = self.m_env.pt.ptui.appid
            self.m_login_sig = r.cookies['pt_login_sig']
            self.m_s_url = self.m_env.pt.ptui.s_url
            return True
        else:
            logging.error("%s fail" % self.m_func)
            return False

    def c_login_2(self):
        ''' 获取 qq加密js'''
        self.m_url = self.m_c_login_2_url
        self.m_func = '[c_login_2]'
        headers = {}
        headers.update(self.m_headers)
        # headers['Referer'] = self.m_xlogin_url
        r = self.m_s.get(self.m_url, headers=headers)
        encoding = chardet.detect(r.content)['encoding']
        r.encoding = encoding[0]
        if r.status_code == requests.codes.ok:
            logging.info("%s ok " % self.m_func)
            return True
        else:
            print '%s fail' % self.m_func
            return False

    def check(self):
        '''check url 获取验证码和salt'''
        self.m_func = '[check]'
        urlplayoud = {
                'regmaster': self.m_regmaster,
                'pt_tea' : 1,
                'pt_vcode': self.m_pt_vcode,
                'uid' : self.m_usernmae,
                'appid' : self.m_appid,
                'js_ver' : self.m_js_ver,
                'js_tpe': self.m_js_type,
                'login_sig': self.m_login_sig,
                'u1':self.m_s_url,
                'uin':self.m_usernmae
                }
        urlplayoud = urllib.urlencode(urlplayoud)

        self.m_url = 'https://ssl.ptlogin2.qq.com/check?' + urlplayoud
        logging.debug("===%s ok===" % self.m_func)
        headers = {}
        headers['Referer'] = self.m_xlogin_url
        r = self.m_s.get(self.m_url, headers=headers, proxies=self.m_proxies, verify=False)
        if r.status_code == requests.codes.ok:
            logging.info("===%s ok===" % self.m_func)
            pattent = r"'(.*?)','(.*?)','(.*?)','(.*?)','(.*?)'"
            lsFind = re.findall(pattent, r.content)
            if lsFind:
                self.m_check_ret = lsFind[0][0]  # ptui_checkVC第1位参数
                self.m_cap_cd = lsFind[0][1]  # ptui_checkVC 第2位参数 验证码
                self.m_salt = lsFind[0][2]  # check ptui_checkVC 第3位参数
                self.m_pt_verifysession = lsFind[0][3]  # ptui_checkVC 第4位参数
                self.m_isRandSale = lsFind[0][4]  # ptui_checkVC 最后5位参数

            if requests.utils.dict_from_cookiejar(r.cookies).has_key('ptvfsession'):
                self.m_ptvfsession = r.cookies['ptvfsession']
                return True
            else:
                logging.error('%s fail %s' % (self.m_func, r.content))
                logging.error('%s fail ptvfsession == NULL' % self.m_func)
                return False
        else:
            logging.error("%s fail" % self.m_func)
            return False

    def login(self):
        ''' 登陆 '''
        self.m_func = '[login]'
        js_encrypt = open('encryption.js', 'rb').read()
        self.jsparse(js_encrypt)
        urlplayoud = {
                'u' : self.m_usernmae,
                'pt_vcode_v1' : 0,
                'pt_verifysession_v1' : self.m_ptvfsession,
                'pt_randsalt' : self.m_isRandSale,
                'u1' : 'http://t.qq.com',
                'ptredirect' : 1,
                'h' : 1,
                't' : 1,
                'g' : 1,
                'from_ui' : 1,
                'ptlang' : '2052',
                'action' : '0-21-1083992',  # '6' + "-" + '16' + "-" + str(time.time()).replace('.', '')[0:13],
                'js_ver' : 10135,
                'js_type' : 1,
                'login_sig' : self.m_login_sig,
                'pt_uistyle' : 23,
                'low_login_enable' : 1,
                'low_login_hour' : 720,
                'aid' : self.m_appid,
                'daid' : 6
                }



        logging.info('%s' % urllib.urlencode(urlplayoud))
        self.m_url = 'https://ssl.ptlogin2.qq.com/login?' + urllib.urlencode(urlplayoud)
        logging.info('user=%s,pwd=%s,cap_cd=%s', self.m_usernmae, self.m_password, self.m_cap_cd)

        # 获取qq加密密码
        enc_pwd = self.m_env.getQQPassString(self.m_password, self.m_usernmae, self.m_cap_cd)

        logging.info('enc_pwd=%s,len=%d', enc_pwd, len(enc_pwd))
        self.m_url = self.m_url + '&p=' + enc_pwd
        self.m_url = self.m_url + "&verifycode=" + self.m_cap_cd
        self.m_url = self.m_url + "&"
        headers = {
                'Referer': self.m_xlogin_url
                }

        self.m_s.cookies.update({'ptui_loginuin': self.m_usernmae})
        r = self.m_s.get(self.m_url, headers=headers, proxies=self.m_proxies, verify=False)
        if r.status_code == requests.codes.ok:
            logging.info("%s ok" % self.m_func)
            pattent = r"'(.*?)','(.*?)','(.*?)'"
            lsFind = re.findall(pattent, r.content)
            if lsFind:
                self.m_check_sig_url = lsFind[0][2]
            return True
        else:
            logging.error("%s fail" % self.m_func)
            return False

    def check_sig_url(self):
        ''' 获取cookie 字符串'''
        self.m_url = self.m_check_sig_url
        self.m_func = '[check_sig_url]'
        r = self.m_s.get(self.m_url)
        if r.status_code == requests.codes.ok:
            logging.info('%s ok' % self.m_func)
            cookie_dic = requests.utils.dict_from_cookiejar(self.m_s.cookies)
            return self.dump_c(cookie_dic)
        else:
            logging.error("%s fail" % self.m_func)
            return ""






if __name__ == '__main__':

    username = '295044696'
    password = 'aA1234567890'
    # account_hex = '\x00\x00\x00\x00\x11\x96\x06\x58'
    weibo = weibo_login()
    weibo.jsparse_path('encryption.js')
    weibo.set_userinfo(username, password)

    bret = weibo.t_qq_login_page()
    if not bret:
        sys.exit(1)
    bret = weibo.xlogin_iframe()
    if not bret:
        sys.exit(1)
    bret = weibo.check()
    if not bret:
        sys.exit(1)
    bret = weibo.login()
    if not bret:
        sys.exit(1)
    print weibo.check_sig_url()
