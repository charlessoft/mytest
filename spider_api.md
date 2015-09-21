# 用于普通站点
common/setting
[
	{
		'id':int,               # id
		'name': str,            # 名称
		'url':str,              # url
		'type':str,             # 类型（一般站点可能无用）
		'js_on': bool,          # 启用js
		'proxy_on': bool,       # 启用代理
		'max_depth': int,  		# 最大深度
	},
	...
]

# 用于预定义的站点
regular/setting:
[
	{
		'id':int,               # id
		'name': str,            # 名称
		'type':str,             # 类型
		'js_on': bool,          # 启用js
		'proxy_on': bool,       # 启用代理
		'max_depth': int,  		# 最大深度
	},
	...
]

# IP   要不要加id ？
[(ip, port), ...]

ip:port 存在则更新，不存在则插入

删除也是同一参数


# bloger  要不要加id ？
[(type, userid),...]

type:userid 存在则更新，不存在则插入

删除也是同一参数


# keywords
{
	type: [word, word ....]
}

直接整体更新