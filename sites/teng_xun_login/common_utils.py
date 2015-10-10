
# -*- coding: UTF-8 -*-
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#from yunsu import *
def write_to_file(str_data, filename):
    with open(filename,'wb') as f:
        f.write(str_data)
        f.close()

def append_to_log(str_data, filename):
    with open(filename,"ab") as f:
        f.write(str_data)
        f.write('\n')
        f.close()

def dic_to_str(dic):
    str = ""
    for k,v in dic.items():
        str = str + '%s:%s\n' %(k,v)
    return str

def dump_map(dic):
    str = ""
    for k,v in dic.items():
        str = str + '%s: %s\n' %(k,v)

    return str

def dump_response(r):
    str_data = ""
    str_data = str_data + 'HTTP/1.1 ' + str(r.status_code)  + '\n'

    str_data = str_data + dump_map(r.headers)
    return str_data

def mylog(func_name,url, method_name,cookies,headers,r,data,log_name,bsave_conntent=True):
    append_to_log(func_name,log_name)
    append_to_log(method_name,log_name)
    append_to_log(url,log_name)
    append_to_log(dic_to_str(cookies),log_name)
    append_to_log(dic_to_str(headers),log_name)
    if len(data)>0:
        if str(type(data)) == "<type 'dict'>":
            append_to_log(dic_to_str(data),log_name)
        else:
            append_to_log(data,log_name)


    append_to_log(dump_response(r),log_name)
    if bsave_conntent:
       append_to_log(r.content,log_name)
    append_to_log('=========================',log_name)

def ysdm( img_path ):
    client = APIClient()
    paramDict = {}
    result = ''
    paramDict['username'] = 'studio20130101'
    paramDict['password'] = 'helloworld11'
    paramDict['typeid'] = '5000'
    paramDict['timeout'] = '60'
    paramDict['softid'] = '16117'
    paramDict['softkey'] = '3255105d16024f81af866a85b68a5c1d'
    imagePath = img_path #'c:\\code.jpg'
    print 'ysdm: path=' + imagePath
    paramKeys = [
         'username',
         'password',
         'typeid',
         'timeout',
         'softid',
         'softkey'
        ]
    import Image
    img = Image.open(imagePath)
    if img is None:
        print 'get file error!'
        sys.exit(1)
    img.save("upload.gif", format="gif")
    filebytes = open("upload.gif", "rb").read()
    result = client.http_upload_image("http://api.ysdm.net/create.xml", paramKeys, paramDict, filebytes)
    print result
    return result


def get_cur_time():
    return str(time.time())[0:-3]
