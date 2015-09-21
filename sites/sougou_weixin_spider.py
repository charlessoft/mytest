# -*- coding: UTF-8 -*-
from selenium import webdriver
from pyvirtualdisplay import Display
import time,re,urllib,tablib
#display = Display(visible=0, size=(800, 600))
#display.start()

#使用 selenium 和phantomjs

driver = webdriver.PhantomJS()
driver.get('http://weixin.sogou.com/weixin?type=2&query=%E8%BD%A6%E5%BA%93%E5%92%96%E5%95%A1&ie=utf8')
login_button=driver.find_element_by_id("searchBtn")
login_button.click()

driver.implicitly_wait(120)
time.sleep(3)

print 'handle count = %d' % len(driver.window_handles)
#for handle in driver.window_handles:
    #print handle
        #driver.switch_to_window(handle)
url=driver.current_url
print url
article_link1 = driver.find_element_by_id('sogou_vr_11002601_title_0')
article_link1.click()
print 'handle count = %d' % len(driver.window_handles)
#nindex = -1
source_file='tmp.html'
time.sleep(3)
#for handle in driver.window_handles:
    #print handle
    #url=driver.current_url
    #print url
    #html=driver.page_source
    #nindex=nindex+1
    #driver.switch_to_window(handle)
    ##driver.switch_to_window(driver.window_handles[nindex])
    #time.sleep(3)
if len(driver.window_handles)>1:
    driver.switch_to_window(driver.window_handles[1])
    html = driver.page_source
    open(source_file,'wb').write(html.encode('utf-8'))


#p=re.compile('token=\d.*')
#token=p.findall(url)[0]
#print token
#num=0
#data=[]
#k=0
#while num<30:
    #url_message='https://mp.weixin.qq.com/cgi-bin/message?t=message/list&action=&keyword=&offset=%s&count=20&day=7&filterivrmsg=&%s&lang=zh_CN' % (num,token)
    #num+=20
    #driver.get(url_message)
    #html=driver.page_source

    #s=re.compile('list : ([\d\D].*)\.msg_item\,')
    #value=eval(s.findall(html)[0])
    #for i in range(20):
        #try:
            #item=value["msg_item"][i]
            #fakeid=item["fakeid"]
            #nickname=item["nick_name"]
            #date_time=item["date_time"]
            #content=item["content"]
            #head_url='https://mp.weixin.qq.com/cgi-bin/getheadimg?%s&fakeid=%s'%(token,fakeid)
            #driver.get(head_url)
            #print fakeid,nickname,date_time,content
            #data.append([fakeid,nickname,date_time,content])
            #driver.save_screenshot('%s.png' % (fakeid))
        #except:
            #break

#headers = ('fakeid', 'nickname','datetime','content')
#data = tablib.Dataset(*data, headers=headers)
#with open(u'data.xls', 'wb') as f:
    #f.write(data.xls)

#driver.quit()
