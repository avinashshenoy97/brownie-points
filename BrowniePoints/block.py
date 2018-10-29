'''
Script for Block data structure and its properties.
'''
# ==================== Imports ==================== #
from hashlib import sha256
from datetime import datetime as dt
from json import JSONEncoder
from dateutil.parser import parse as dtparser


# ==================== Main ==================== #
class block:

    def __init__(self, index, hash, previousHash, timestamp, data, difficulty, nonce):
        self.index, self.hash, self.previousHash, self.timestamp, self.data,self.difficulty,self.nonce = \
            (index, hash, previousHash, timestamp, data, difficulty, nonce)

    def __eq__(self, other):
        return self.hash == other.hash

    def deserialize(d):
        '''Creates a block object from a dict/json.

        d: the dict/json containing index, hash, previousHash, timestamp, data, difficulty, nonce as keys

        Returns:
            A block object.
        '''
        
        return block(d['index'], d['hash'], d['previousHash'], dtparser(d['timestamp']), d['data'], d['difficulty'], d['nonce'])
    


class blockEncoder(JSONEncoder):
    def default(self, b):
        try:
            return b.__dict__
        except:
            return str(b)