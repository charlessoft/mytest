# -*- coding: UTF-8 -*-
import time
import requests
import urllib
# import yunsu
from common_utils import *
import sys
import re
import xml.dom.minidom
import string
import random
import chardet

import logging

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

# logging.debug('This is debug message')
# logging.info('This is info message')
# logging.warning('This is warning message')
# from browser import *
# from w3c import *
# import w3c
# import browser
from pyquery import PyQuery as pq
# import PyV8
# from PyV8 import *
from pyv8 import PyV8

reload(sys)
sys.setdefaultencoding('utf-8')
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


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
        # if self.m_cookies:
        # return m_cookies
        # else:
        # self.m_cookies = v8Cookie()
        # logging.info("sssss");
        # return m_cookies


        # @property
        # def addEventListener(self):
        # pass

        # def addEventListener(self,domcon,funcname):
        # pass


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


glob = Global()


class weibo_login():
    def set_userinfo(self, username, password):
        self.m_usernmae = username
        self.m_password = password

    def __init__(self):
        logging.info("init")
        self.m_proxies = {
            #'http': '192.168.31.128:8888',
            #'https': '192.168.31.128:8888',
        }
        self.m_usernmae = ''
        self.m_password = ''
        self.m_headers = {}
        self.m_headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
        self.m_wbilang_10000 = ''
        self.m_cookies = {}
        self.m_xlogin_url = ''
        self.m_env = None
        self.m_c_login_2_url = ''
        self.m_ptui_ver_js_url = ''
        self.m_s = requests.session()
        self.m_s.headers.update({
                                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36'})
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

        pass

    def dump_c(self, cookies):
        strtmp = ''
        for key, value in cookies.items():
            strtmp = strtmp + '%s=%s;' % (key, value)

        return strtmp

    def dump_cookie(self, r):
        logging.info("cookie:")
        for key, value in r.cookies.items():
            # print '%s=%s' % (key,value)
            logging.debug('%s=%s;' % (key, value))

    def jsparse_path(self, jspath):
        jscontent = open(jspath, 'rb').read()
        self.jsparse(jscontent)

    def jsparse(self, js):
        ctxt = PyV8.JSContext(glob)
        ctxt.enter()
        ctxt.eval(js)
        self.m_env = ctxt.locals
        # vars = ctxt.locals
        # print vars.g_cdn_js_fail
        # var_i = vars.var_s
        # print var_i
        # ctxt.locals['loadJs']()

        # print ctxt.locals[funname]()
        pass

    def t_qq_login_page(self):
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
                self.dump_cookie(r)
                print r.cookies
                return True
            else:
                logging.error('no search')
                return False

    def xlogin_iframe(self):
        self.m_url = self.m_xlogin_url
        self.m_func = '[xlogin_iframe]'
        # logging.debug(self.m_func)
        headers = {}
        # cookies = {}
        headers.update(self.m_headers)
        headers['Referer'] = 'http://t.qq.com/login.php'
        headers['Upgrade-Insecure-Requests'] = '1'
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
            # print 'ptui_ver_js_url: %s' % self.m_ptui_ver_js_url
            logging.info("ptui_ver_js_url:%s" % self.m_ptui_ver_js_url)
            # write_to_file(d("script").text(),'1.js')

            self.m_regmaster = self.m_env.pt.ptui.regmaster
            self.m_pt_vcode = self.m_env.pt.ptui.pt_vcode_v1
            self.m_appid = self.m_env.pt.ptui.appid
            self.m_login_sig = r.cookies['pt_login_sig']
            self.m_s_url = self.m_env.pt.ptui.s_url
            print '\n'
            return True
            # print len(self.m_cookies)
            # print self.m_cookies
            # print r.content
            # print r.text
        else:
            # print '%s fail' % self.m_func
            logging.error("%s fail" % self.m_func)
            return False

    def url_build(self, domain, urlplayoud):
        strurl = ''
        for item in urlplayoud.items():
            strurl = strurl + '%s=%s&' % (item[0], item[1])
            ##strurl = strurl + urllib.urlencode(item)
            # print urllib.urlencode(item)
            # print item
        return domain + strurl[0:-1]

    def check(self):
        self.m_func = '[check]'
        urlplayoud = {}
        urlplayoud['regmaster'] = self.m_regmaster
        urlplayoud['pt_tea'] = 1
        urlplayoud['pt_vcode'] = self.m_pt_vcode
        urlplayoud['uid'] = self.m_usernmae
        urlplayoud['appid'] = self.m_appid
        urlplayoud['js_ver'] = self.m_js_ver
        urlplayoud['js_tpe'] = self.m_js_type
        urlplayoud['login_sig'] = self.m_login_sig
        urlplayoud['u1'] = self.m_s_url
        urlplayoud['uin'] = self.m_usernmae
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
        self.m_func = '[login]'
        js_encrypt = open('encryption.js', 'rb').read()
        self.jsparse(js_encrypt)
        urlplayoud = {}
        urlplayoud['u'] = self.m_usernmae
        urlplayoud['pt_vcode_v1'] = 0
        urlplayoud['pt_verifysession_v1'] = self.m_ptvfsession
        urlplayoud['pt_randsalt'] = self.m_isRandSale
        urlplayoud['u1'] = 'http://t.qq.com'
        urlplayoud['ptredirect'] = 1
        urlplayoud['h'] = 1
        urlplayoud['t'] = 1
        urlplayoud['g'] = 1
        urlplayoud['from_ui'] = 1
        urlplayoud['ptlang'] = '2052'
        urlplayoud['action'] = '6' + "-" + '40' + "-" + str(time.time()).replace('.', '')[0:13]
        urlplayoud['js_ver'] = 10135
        urlplayoud['js_type'] = 1
        urlplayoud['login_sig'] = self.m_login_sig
        urlplayoud['pt_uistyle'] = 23
        urlplayoud['low_login_enable'] = 1
        urlplayoud['low_login_hour'] = 720
        urlplayoud['aid'] = self.m_appid
        urlplayoud['daid'] = 6
        # print urlplayoud['action']

        logging.info('%s' % urllib.urlencode(urlplayoud))
        # self.m_url = 'https://ssl.ptlogin2.qq.com/check?' + urlplayoud
        self.m_url = 'https://ssl.ptlogin2.qq.com/login?' + urllib.urlencode(urlplayoud)
        # urlplayoud['p'] = self.m_env.enc_pwd(self.m_password,self.m_salt,self.m_cap_cd,False)
        # urlplayoud['verifycode'] = self.m_cap_cd
        # print self.m_password
        # print self.m_salt
        # print self.m_cap_cd
        # print len(self.m_env.enc_pwd('cq3432308851220','\x00\x00\x00\x00\x00\x75\x0f\x05','!VXP',False))
        # print len(self.m_env.enc_pwd('cq3432308851220','\x00\x00\x00\x00\x00\x75\x0f\x05','!BFU',False))
        # print len(self.m_env.enc_pwd(self.m_password,'\x00\x00\x00\x00\x00\x75\x0f\x05',self.m_cap_cd,False))

        # print len(self.m_env.test())
        # sys.exit(1)
        # aa= '\x00\x00\x00\x00\x00\x75\x0f\x05'
        # print repr(self.m_salt)
        # weibo.m_env['test11'](self.m_salt)
        # sys.exit(1)
        self.m_url = self.m_url + '&p=' + self.m_env.enc_pwd(self.m_password, '\x00\x00\x00\x00\x00\x75\x0f\x05',
                                                             self.m_cap_cd, False)
        self.m_url = self.m_url + "&verifycode=" + self.m_cap_cd
        self.m_url = self.m_url + "&"
        headers = {}
        headers['Referer'] = self.m_xlogin_url
        # print urllib.urlencode(urlplayoud)
        # print self.m_url
        self.m_s.cookies.update({'ptui_loginuin': self.m_usernmae})
        r = self.m_s.get(self.m_url, headers=headers, proxies=self.m_proxies, verify=False)
        if r.status_code == requests.codes.ok:
            logging.info("%s ok" % self.m_func)
            logging.info("%s " % r.content)

            pattent = r"'(.*?)','(.*?)','(.*?)'"
            lsFind = re.findall(pattent, r.content)
            if lsFind:
                self.m_check_sig_url = lsFind[0][2]
                # self.m_check_ret = lsFind[0][0] #ptui_checkVC第1位参数
                # self.m_cap_cd = lsFind[0][1] #ptui_checkVC 第2位参数 验证码
                # self.m_salt = lsFind[0][2] # check ptui_checkVC 第3位参数
                # self.m_pt_verifysession = lsFind[0][3] #ptui_checkVC 第4位参数
                # self.m_isRandSale = lsFind[0][4] #ptui_checkVC 最后5位参数
                # for cookie in r.cookies:
                # print cookie
            # self.dump_cookie(r)
            return True
        else:
            logging.error("%s fail" % self.m_func)
            return False
            # print r.content
            # r = self.m_s.get(self.m_url,headers=headers,proxies=self.m_proxies,verify=False)
            # print r.status_code

    def check_sig_url(self):
        self.m_url = self.m_check_sig_url
        self.m_func = '[check_sig_url]'
        r = self.m_s.get(self.m_url)
        if r.status_code == requests.codes.ok:
            logging.info('%s ok' % self.m_func)
            cookie_dic = requests.utils.dict_from_cookiejar(self.m_s.cookies)
            # //self.dump_cookie(cookie_dic)
            print self.dump_c(cookie_dic)
            # for cookie in self.m_s.cookies:
            #     print cookie[0]
            # for cooike in self.m_s.cookies:
            # print cookie
            # for cookie in r.cookies:
            # print cookie
        else:
            logging.error("%s fail" % self.m_func)





            # print str(urlplayoud)

    def c_login_2(self):
        self.m_url = self.m_c_login_2_url
        self.m_func = '[c_login_2]'
        headers = {}
        headers.update(self.m_headers)
        # headers['Referer'] = self.m_xlogin_url
        r = self.m_s.get(self.m_url, headers=headers)
        encoding = chardet.detect(r.content)['encoding']
        r.encoding = encoding[0]
        if r.status_code == requests.codes.ok:
            # print '%s ok' % self.m_func
            logging.info("%s ok " % self.m_func)
            # write_to_file(d('script').text(),'2.js')
            # write_to_file(r.content,'2.js')
            # self.jsparse(open('2.js','rb').read())
            # self.jsparse(r.content)

            return True
        else:
            print '%s fail' % self.m_func
            return False

    def ptui_ver(self):
        self.m_func = '[ptui_ver]'
        self.m_url = 'https://xui.ptlogin2.qq.com/ptui_ver.js?v=0.5547120401170105&ptui_identifier=000D5A63AFD8E43E31F56095BF5ABDAC41EDDBFB1BD451D648BD1F54'


if __name__ == '__main__':
    username = ''
    password = ''
    #'\x00\x00\x00\x00\x00\x75\x0f\x05',
#密码加密为qq号16进制,可以改成用js生成来调用.
    weibo = weibo_login()
    weibo.jsparse_path('encryption.js')
    s = '%s' % weibo.m_env['get_new_date']()
    #weibo.set_userinfo('7671557', '')
    weibo.set_userinfo(username,password)
    # weibo.jsparse('')
    # print weibo.m_env['match']
    # print weibo.m_env['new']['Date']()
    # sys.exit(1)
    bret = weibo.t_qq_login_page()
    if bret != True:
        sys.exit(1)
    bret = weibo.xlogin_iframe()
    if bret != True:
        sys.exit(1)
    bret = weibo.check()
    if bret != True:
        sys.exit(1)
    bret = weibo.login()
    if bret != True:
        sys.exit(1)
    bret = weibo.check_sig_url()

    # bret = weibo.c_login_2()
    # if bret != True:
    # sys.exit(1)



    # xloginjs = open('1.js','rb').read()
    # weibo.jsparse(xloginjs,'loadJs')
    # print weibo.m_env['Math']['random']()
    # print weibo.m_env.pt.ptui.s_url
    # doc = w3c.parseString(xloginjs)
    # print doc
    # win = HtmlWindow(TEST_URL,doc)


    # weibo.jsparse(xloginjs)
    # weibo.jsparse('''
    # z=function test()
    # {
    # return 1+2;
    # }
    # ''')

    # (function(){
    # function hello(){
    # return "Hello world.";
    # }
    # return hello();
    # })
    # ''')
