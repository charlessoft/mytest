# 验证 HTTPBasicAuth

# status_code : OK 200
				argument error 400
				not found 404
				other 500

# 爬取数据 接口
	
	url: http://localhost:5000/spider/article

	# 获取

		method： GET
		query_string_arguments:
			argument('keywords', action='append', help='document keyword list')
			argument('tags', action='append')
			argument('offset', type=int)
			argument('limit', type=int)
			argument('time_start', type=int, required=True)
			argument('time_end', type=int, required=True)
		return:
			[
				{
					'authors':str,
					'keywords':str, // 要讨论是否设置成list
					'tags':str, // 要讨论是否设置成list
					'title':str,
					'text':str,
					'publish_date': str, // or float
					'updatetime': float,
					'url': str
				},
				...
			]

		example:

			url: http://localhost:5000/spider/article?time_start=1&time_end=1441866812&offset=0&limit=50&keywords=0&keywords=2&tags=2

			r = requests.get('http://localhost:5000/spider/article', params={'time_start':1, 'time_end':1441866812, 'keywords':['0', '2'], tags=['2'], 'offset':0, 'limit'=50}, auth=auth)

			return:
				[{u'authors': u'00000',
				  u'keywords': u'0',
				  u'publish_date': u'2014-02-03',
				  u'tags': u'0',
				  u'text': u'00000',
				  u'title': u'00000',
				  u'updatetime': 1441859136.5471795,
				  u'url': u'http://00000.com'}
			  	]




# 爬虫配置（单记录）

	url: http://localhost:5000/spider/setting
	
	# 获取 

		method： GET
		query_string_arguments:
			argument('domain', required=True)
			argument('proxy_on', type=bool, default=False)
			argument('js_on', type=bool, default=False)
			argument('max_recurrence', type=int, default=3)

		return:
			{
				'id':int,
				'domain': str,
				'js_on': bool,
				'proxy_on': bool,
				'max_recurrence': int,
				'updatetime': float
			 }

		example:
			r = requests.get('http://localhost:5000/spider/setting', params={'domain': '22222' }, auth=auth, headers=headers)
			return:
				{
					'id':int,
					u'domain': u'22222',
					u'js_on': True,
					u'max_recurrence': 2,
					u'proxy_on': False,
					u'updatetime': 1441918637.904374
				}

	# 增加/修改
		method： PUT
		json:
			{
				'domain': str,
				'js_on': bool,
				'proxy_on': bool,
				'max_recurrence': int,
				'updatetime': float
			 }

		return:
			null

		example:
			r = requests.put('http://localhost:5000/spider/setting', json={'proxy_on': False, 'max_recurrence': '2', 'domain': '22222', 'updatetime': 1441918637.904374, 'js_on': True}, auth=auth, headers=headers)


	# 删除
		method： DELETE
		query_string_arguments:
			argument('domain', required=True)
		return:
			null

		example:
			r = requests.delete('http://localhost:5000/spider/setting', params={'domain': '22222' }, auth=auth, headers=headers)


# 爬虫配置（多记录）

	url: http://localhost:5000/spider/setting/list
	
	# 获取

		method： GET
		return:
			[
				{
					'domain': str,
					'js_on': bool,
					'proxy_on': bool,
					'max_recurrence': int,
					'updatetime': float
				},
				...
			 ]

		example:
			r = requests.get('http://localhost:5000/spider/setting/list', auth=auth, headers=headers)
			return:
				[
					{
						u'domain': u'22222',
						u'js_on': True,
						u'max_recurrence': 2,
						u'proxy_on': False,
						u'updatetime': 1441918637.904374
					},
					...
			 	]


	# 增加/修改
		method： PUT
		json:
			[
				{
					'domain': str,
					'js_on': bool,
					'proxy_on': bool,
					'max_recurrence': int,
					'updatetime': float
				},
				...
			 ]

		return:
			null


	# 删除
		method： DELETE
		json:
			[domain1, domain2, domain3]
		return:
			null


ip:
[(id, ip, port), ...]



keywords:
{
	type: []
}



bloger:
[(id, type, userid),...]