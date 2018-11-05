'''
Script for Block data structure and its properties.
'''
# ==================== Imports ==================== #
from hashlib import sha256
from datetime import datetime as dt
import json
from dateutil.parser import parse as dtparser
from copy import deepcopy
from collections import OrderedDict

import transaction


# ==================== Main ==================== #
class block:

	def __init__(self, index, hash, previousHash, timestamp, data, difficulty, nonce):
		self.index, self.hash, self.previousHash, self.timestamp, self.data,self.difficulty,self.nonce = \
			(index, hash, previousHash, timestamp, data, difficulty, nonce)

	def __eq__(self, other):
		return self.hash == other.hash

	def __str__(self):
		d = deepcopy(self.__dict__)
		d['data'] = list()
		for data in d['data']:
			d['data'].append(str(data))

		return str(OrderedDict([(key, d[key]) for key in sorted(d)]))

	def deserialize(d):
		'''Creates a block object from a dict/json.

		d: the dict/json containing index, hash, previousHash, timestamp, data, difficulty, nonce as keys

		Returns:
			A block object.
		'''
		data = list()
		for da in d['data']:
			data.append(transaction.Transaction.deserialize(da))
		return block(d['index'], d['hash'], d['previousHash'], dtparser(d['timestamp']), data, d['difficulty'], d['nonce'])

	def calculateHash(self):
		'''Calculates hash for given block.

		Returns:
			SHA256 hash of block.
		'''
		data = list()
		for d in self.data:
			data.append(str(d))
		preHashedString = str(self.index) + self.previousHash + str(self.timestamp) + str(data) + str(self.difficulty) + str(self.nonce)
		return sha256(bytes(preHashedString, 'utf-8')).hexdigest()
	


class customEncoder(json.JSONEncoder):
	def default(self, b):
		try:
			return b.__dict__
		except:
			return str(b)
