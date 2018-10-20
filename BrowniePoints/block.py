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

    @classmethod
    def calculateHash(cls,index, previousHash, timestamp, data, nonce):
        '''Calculates a block's hash, given its index, the previous block's hash, its timestamp, its data and its nonce.

        Arguments:
            index: the block's index.

            previousHash: the hash of the block behind the given block in the chain.

            timestamp: the timestamp of the block.

            data: the data of the block.

            nonce: nonce value for the block
        Returns:
            The hash string (in hexadecimals) of the given data.
        '''
        preHashedString = str(index) + previousHash + str(timestamp) + data + str(nonce)
        return sha256(bytes(preHashedString, 'utf-8')).hexdigest()

    @classmethod
    def hexToBinary(cls, hash_str):
        '''Converts the given input 'hash_str' from hexadecimal to its equivalent binary representation

        :param
            hash_str: hexadecimal string
        :return: string of 256 binary characters, representing the binary value of the hash
        '''
        return bin(int(hash_str, 16))[2:].zfill(256)

    @classmethod
    def hashMatchesDifficulty(cls, hash,difficulty):
        '''Checks if the given hash matches the current difficulty level

        :param
            hash: bit string representing binary value of the hash
            difficulty: current difficulty level of the network
        :return: Boolean
        '''
        binary_hash = block.hexToBinary(hash)
        return binary_hash.startswith('0'*difficulty)

    @classmethod
    def findBlock(cls, index, previousHash, timestamp, data, difficulty):
        '''
        Creates a new valid block by finding the nonce value such that the created block satisfies current difficulty
        :param index: index of the block
        :param previousHash: hash the block preceding the new block
        :param timestamp: time when the new block is created
        :param data: data
        :param difficulty: current difficulty
        :return: New block
        '''
        nonce = 0
        while True:
            hash = cls.calculateHash(index, previousHash, timestamp, data, nonce)
            if cls.hashMatchesDifficulty(hash, difficulty):
                return block(index, hash, previousHash, timestamp, data, difficulty, nonce)

            nonce += 1


class blockEncoder(JSONEncoder):
    def default(self, b):
        try:
            return b.__dict__
        except:
            return str(b)