# QQ 微博登录流程分析

## 1. 概述
---

爬腾讯微博内容，需要登录后才能输入关键字查询，进行爬取，对于爬取网站，基本的流程是通过在搜索、爬取页面时候传递cookies、headers信息来获得相关内容。

## 2. 分析腾讯账号登流程
---

### 2.1. 浏览器登录流程

使用chrome浏览器登录腾讯微博流程，浏览器中输入http://t.qq.com， Chrome会自动访问该页面，并进行解析，把所有的url地址和js脚本都会下载下来，等待用户下一步操作。在用户输入账号和密码后，当点击登录按钮，浏览器会触发js脚本进行加密qq密码，发送给服务器端，完成登录流程。

### 2.2. 分析登录流程


腾讯账号登录过程和普通网站流程不一样，登录步骤需要5步，登录过程全部采用GET求情，所以只要分析完5个 请求的详细流程，就能实现登录。


![图 1](http://10.142.49.230:9999/udb/udb-spider/uploads/c91d140518a7795c30d8d7014247d6ff/p1.png)

### 2.3. 各步骤登录明细

访问每个请求，都需要保留cookie，其中c_login_2.js、Login_page、xlogin_iframe请求都是前期准备工作，**获取cookie和js等内容**。

#### 2.3.1. c_login_2.js

这个脚本是腾讯服务器返回，用于qq加密流程用，由图1第12步骤下载获得。

#### 2.3.2. login_page

访问该页面是用来获取真实的登录页面，登录页面是以Iframe方式插入到t.qq.com中。

![图 2](http://10.142.49.230:9999/udb/udb-spider/uploads/30706163aef8713126dad1f87a17115b/p2.png)

#### 2.3.3. xLogin_iframe

访问该页面，服务器会返回cookie，保存该页面的js能够获得下个页面需要的参数。
使用js 格式化工具格式化js代码，获得pt.ptui.regmaster, pt.ptui.pt_vcode_v1, pt.ptui.appid, pt.ptui.s_url用来传递给下个请求使用。下图为用js格式化工具解析后的部分js代码。


![图 3](http://10.142.49.230:9999/udb/udb-spider/uploads/190ec2e5bf0dbc1ef488c9c456f24388/p3.png)

#### 2.3.4. check 请求

该请求是qq登录重要的请求，用来获取服务器返回信息，来判断是否需要输入验证码以及加密qq密码。

**Request:**

GET https://ssl.ptlogin2.qq.com/check?regmaster=&pt_tea=1&pt_vcode=1&uin=295044696&appid=46000101&js_ver=10136&js_type=1&login_sig=jfKLPNGdh2tXJZkAcuWcPpwHkrroGs0L--dnOCKs9*SKw0cxaWENe857j1453GnS&u1=http%3A%2F%2Ft.qq.com&r=0.043882212368771434 HTTP/1.1`

**分析参数：**

**regmaster**= `[xLogin_iframe的js获得 pt.ptui.regmaster]`

**pt_tea**=1 `[c_login_2.js pt_tea=1 固定]`

**pt_vcode**=1 `[xLogin_iframe js  pt.ptui.pt_vcode_v1]`

**uin**=295044696 `[qq账号]`

**appid**=46000101 `[xLogin_iframe js pt.ptui.appid]`

**js_ver**=10135 `[xLogin_iframe js pt.ptui.ptui_version]`

**js_type**=1 `[c_login_2.js pt.plogin.js_type]`

**login_sig**= Z `[xLogin_iframe js 返回cookie获得,:pt_login_sig ]`

**u1**=http%3A%2F%2Ft.qq.com `[xLogin_iframe js pt.ptui.s_url]`

**r**=0.17178064701147377 `[随机数]`


**Response:**

![图 4](http://10.142.49.230:9999/udb/udb-spider/uploads/ac28c49302425d566dcc3c3f9452318f/p4.png)

**!XSZ** 为验证码（vcode），默认情况下，服务器返回随机验证码，用户不需要输入，如果该参数为空，就说明需要手动输入验证码。

**'\x00\x00\x00\x00\x11\x96\x06\x58`** (salt)为qq295044696的16进制表示形式

**'c9ce166c76bfe2ad7bxxx'** 为下个请求pt_verifysession_v1需要的参数。

#### 2.3.5. qq加密

QQ登录在第4步登录到时候需要对QQ密码进行加密，该加密过程是在c_login_2.js代码中使用rsa加密。

![图 5](http://10.142.49.230:9999/udb/udb-spider/uploads/0ff6d7a46db65b945b0062367ad2c894/p5.png)

`function getEncryption(password, salt, vcode, isMd5)`

**password:**QQ密码

**salt:**由check请求返回的qq号16进制字符串

**vcode:**由check请求返回的验证码

**isMd5:** 默认为Fasle

JS加密qq，使用js引擎来解析执行，目前是使用V8引擎，需要做的就是把js代码提取出来，通过v8解析能够计算出qq密码就可以。

#### 2.3.6. login

该请求为把qq密码加密后,构造参数发送给服务器。

**Request:**


GET https://ssl.ptlogin2.qq.com/login?u=295044696&verifycode=!XSZ&pt_vcode_v1=0&pt_verifysession_v1=c9ce166c76bfe2ad7bd86e327107e56495e426d4a9e3e05adc2d63ddac54414fd5d6c3808edfe42e8d1daedaed396e614e14b989e98dbef6&p=hm0yYXumYaXDUIqg3ftci8Ep0jI3dHxzTbQKWLkvxxz6i9zGezkydLI5BcoI8RpvY26BL4zlldARDGHfOWHUQoPn-iVImv0fwAGakpYujxpKfmpSixOH83HCYMr7q6dt4Jl66zBgRBxgWmLD6GG4X8lNDzKruVEdsC27Z1sL48730tr-1wF-9SM11uibIrFMqlPS7f25Pp*UCxB8LYuYbA__&pt_randsalt=0&u1=http%3A%2F%2Ft.qq.com&ptredirect=1&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=5-16-1444948427008&js_ver=10136&js_type=1&login_sig=jfKLPNGdh2tXJZkAcuWcPpwHkrroGs0L--dnOCKs9*SKw0cxaWENe857j1453GnS&pt_uistyle=23&low_login_enable=1&low_login_hour=720&aid=46000101&daid=6& HTTP/1.1


**分析参数：**


**u**=295044696 `[qq账号]`

**verifycode**=!XSZ  `[check请求返回的ptui_checkVC 第2个参数(验证码)]`

**pt_vcode_v1**=0  `[xlogin_iframe 返回内容中获得]`

**pt_verifysession_v1**=ece043abxxx `[check 请求的cookieptvfsession获得]`

**p**=zY9LJeXElReVkw__ `[密码加密,调用js加密]`

**pt_randsalt**=0  `[c_login_2.js 的pt.plogin.isRandSalt 获得]`

**u1**=http%3A%2F%2Ft.qq.com `[固定值]`

**ptredirect**=1 `[xlogin_iframe 的 pt.ptui.target获得]`

**h**=1 `[默认]`

**t**=1 `[默认]`

**g**=1 `[默认]`

**from_ui**=1 `[c_login_2.js f.from_ui获得]`

**ptlang**=2052 `[xlogin_iframe 的lang: encodeURIComponent("2052"),获得]`

**action**=6-40-1443767863383 `[按钮的点击数]`

**js_ver**=10135 `[xlogin_iframe ptui_version: encodeURIComponent("10135"),获得]`

**js_type**=1 `[c_login_2.js js_type 获得]`

**login_sig**=II7uLe-SaLQ*jia5PBEiYFqZxxx- `[xlogin_iframe 返回的cookie pt_login_sig获得]`

**pt_uistyle**=23  `[xlogin_iframe 获得  style: encodeURIComponent("23")]`

**low_login_enable**=1 `[c_login_2.js  low_login_enable 获得]`

**low_login_hour**=720 `[c_login_2.js获得]`

**aid**=46000101 `[xlogin js pt.ptui.appid 获得]`

**daid**=6 `[xlogin_iframe daid: encodeURIComponent("6"),获得]`


**Response:**

ptuiCB('0','0','`http://ptlogin4.t.qq.com/check_sig?pttype=1&uin=295044696&service=login&nodirect=0&ptsigx=b9d7cb2f6b5612bd02195ce68a874a265abc38d474d5bf89b41397fea40af3863dea89a21afba4369ea380bfc78d27dadb5ea6e639c24df1a2dc78d6f87722f9&s_url=http%3A%2F%2Ft.qq.com&f_url=&ptlang=2052&ptredirect=101&aid=46000101&daid=6&j_later=0&low_login_hour=720&regmaster=0&pt_login_type=1&pt_aid=0&pt_aaid=0&pt_light=0&pt_3rd_aid=0`','1','`登录成功！`', 'xx ');

返回的第**4**个参数说明登录成功,第**3**个参数url地址就是最终获取的cookie地址,

#### 2.3.7. getcookie


访问cookie的url是通过上一个请求返回的地址，访问该地址就能获取到cookie。


##总结
---

本文档解释了登录腾讯微博的步骤,目前腾讯登录验证会定期做调整,大部分是qq密码加密或者一些参数做调整,对于qq密码加密,只需要提取js代码,通过v8解析能够计算出qq密码就可以。


## 资料
[javascritp \x 16进制](http://stackoverflow.com/questions/7061795/string-encoding-question)



