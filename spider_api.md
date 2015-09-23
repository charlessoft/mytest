# 用于普通站点
common/setting
{
    'settings': [
        {
            'url': str              # url
            'name': str,            # 名称
            'js_on': bool,          # 启用js
            'proxy_on': bool,       # 启用代理
            'max_depth': int,       # 最大深度
        },
        .....
    ]
}

# 用于预定义的站点
regular/setting:
{
    'settings': [
        {
            'name'      : str
            'type'      : str,             # 类型
            'js_on'     : bool,          # 启用js
            'proxy_on'  : bool,       # 启用代理
            'max_depth' : int,       # 最大深度
        },
        ...
    ]
}

# proxies
{
    'proxies': [(ip, port), ...]
}

# bloger 
{
    'type': [userid,....],
}

    bloger.type:
    weixin
    sina_weibo
    qq_weibo
    people_weibo
    xinhua_weibo
    ...


# keywords
{
    'type': [word, word ....],
}

    keywords.type:
    all
    common
    search
    bloger
    ...

# result
队列:redis
类型：list
key名：processor2result  
解码: http://msgpack.org/  
数据结构：(task,result)   # 只要取result就行了
数据结构例子:

(
    {
    u'status': 1, u'project': u'souguo', 'group': None, u'schedule': {u'priority': 2}, u'url': u'http://info.hp.hc360.com/2015/09/220847300302.shtml', 'project_md5sum': '437a98de0797f5d97efb51b3f74d89cd', 'project_updatetime': 1442883132.329, u'process': {u'callback': u'detail_page'}, u'taskid': u'7c1c70ac7fb547e688fbc860746b2c75', u'fetch': {u'headers': {u'User-Agent': u'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'}}
    }, 
    {
    'url': 'http://info.hp.hc360.com/2015/09/220847300302.shtml', 
    'type': 'type',
    'html':'xxxxxxx',
    'title': 'xxxxx',
    'text':'xxxxx', 
    'authors' : 'xxxx|xxxx',
    'publish_time': 1442884792.59
    }
)