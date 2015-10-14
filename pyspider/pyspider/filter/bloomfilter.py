#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: kasim
# Created on 2015-08-14 22:23:10

import logging
import pybloom
import os
from six.moves.urllib.parse import urlparse

try:
	import pyreBloom
except ImportError:
	pass

logger = logging.getLogger('filter')


###  pyreBloom

# >>> p.add('xxxx')
# 1
# >>> p.add('xxxx')
# 0
# >>> p.add('xxxx')
# 0

# >>> p.contains('xxx')
# True
# >>> p.contains(['xxx'])
# ['xxx']
# >>> p.contains(['dsds'])
# []

############################

###  pybloom

# >>> bf.add('rrrr')
# False
# >>> bf.add('rrrr')
# True
# >>> bf.add('rrrr')
# True


class BaseFilter(object):
	def __init__(self, *args, **kwargs):
		self._quit = False

	def add(self, value):
		raise NotImplementedError

	def extend(self, values):
		raise NotImplementedError

	def contains(self, values):
		raise NotImplementedError

	def tofile(self, key):
		pass

	def fromfile(self, key):
		pass

	def run(self):
		import time
		while not self._quit:
			try:
				time.sleep(1000)
			except KeyboardInterrupt:
				self.quit()
				logger.info("bloomfilter loop exiting...")
				break

	def quit(self):
		'''Quit bloomfilter'''
		self._running = False
		self._quit = True
		self.tofile()

	def xmlrpc_run(self, port=13100, bind='127.0.0.1', logRequests=False):
		'''Run xmlrpc server'''
		import umsgpack
		try:
			from xmlrpc.server import SimpleXMLRPCServer
			from xmlrpc.client import Binary
		except ImportError:
			from SimpleXMLRPCServer import SimpleXMLRPCServer
			from xmlrpclib import Binary

		logger.info("bloomfilter starting...")

		server = SimpleXMLRPCServer((bind, port), allow_none=True, logRequests=logRequests)
		server.register_introspection_functions()
		server.register_multicall_functions()

		server.register_function(self.quit, '_quit')

		server.register_function(self.add, 'add')

		server.timeout = 0.5
		while not self._quit:
			server.handle_request()

		logger.info("bloomfilter exiting...")
		server.server_close()


class RedisBloomFilter(BaseFilter):
	def __init__(self, key, capacity=100000, error_rate=0.001, host='127.0.0.1', port=6379, db=0, password=''):
		super(RedisBloomFilter, self).__init__()
		self.bf = pyreBloom.BloomFilter(key, capacity=capacity, error_rate=error_rate, host='127.0.0.1', port=6379, db=0)

	def add(self, value):
		return not bool(self.bf.add(value))

	def extend(self, values):
		return self.bf.extend(values)

	def contains(self, values):
		return self.bf.contains(values)



class BloomFilter(BaseFilter):
	def __init__(self, key, capacity=100000, error_rate=0.001, store_dir=None):
		super(BloomFilter, self).__init__()
		if not store_dir:
			store_dir = os.path.expanduser('~')
		elif not os.path.exists(store_dir):
			os.makedirs(store_dir)

		self.key = key
		self.path = os.path.join(store_dir, key)

		self.bf = pybloom.BloomFilter(capacity=capacity, error_rate=error_rate)
        # self.fromfile()


	def add(self, value):
		return self.bf.add(value)

	def extend(self, values):
		if hasattr(values, '__iter__'):
			return [self.bf.add(v) for v in value]
		else:
			return [self.bf.add(v)]

	def contains(self, values):
		# follow pyreBloom's contains behavious
		if hasattr(values, '__iter__'):
			return [v in self.bf for v in value]
		else:
			return values in self.bf

	def tofile(self):
		logger.info("save data to %s" % self.path)
		with open(self.path, 'wb') as f:
			self.bf.tofile(f)

	def fromfile(self):
		if os.path.exists(self.path):
			try:
				with open(self.path, 'rb') as f:
					self.bf = self.bf.__class__.fromfile(f)
			except Exception as e:
				print('BloomFilter fromfile error: %s' % e)
			else:
				print('BloomFilter load data from: %s' % self.path)


if __name__ == '__main__':
	# bf = pybloom.BloomFilter(10000, 0.0001)
	# import random
	# s = str(random.random())
	# print bf.add(s)
	# print bf.add(s)
	# print bf.add(s)

	# path = 'xxx.txt'

	# with open(path, 'wb') as f:
	# 	bf.tofile(f)

	# with open(path, 'rb') as f:
	# 	bf2 = pybloom.BloomFilter.fromfile(f)

	# print bf2.add(s)


	bf = BloomFilter('pyspider', 10000, 0.0001)
	import random
	s = str(random.random())
	print bf.add(s)
	print bf.add(s)
	print bf.add(s)

	bf.tofile()

	bf2 = BloomFilter('pyspider', 10000, 0.0001)
	bf2.fromfile()

	print bf2.add(s)