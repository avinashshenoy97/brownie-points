'''
Script for Block data structure and its properties.
'''
# ==================== Imports ==================== #
from hashlib import sha256
from datetime import datetime as dt


# ==================== Main ==================== #
class block:

    def __init__(self, index, hash, previousHash, timestamp, data,difficulty,nonce):
        self.index, self.hash, self.previousHash, self.timestamp, self.data,self.difficulty,self.nonce =\
            (index, hash, previousHash, timestamp, data,difficulty,nonce)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def calculateHash(index, previousHash, timestamp, data,nonce):
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

    def hexToBinary(self,hash_str):
        '''Converts the given input 'hash_str' from hexadecimal to its equivalent binary representation

        :return: string of 256 binary characters, representing the binary value of the hash
        '''
        return bin(int(hash_str, 16))[2:].zfill(256)

    def hashMatchesDifficulty(self,hash):
        binary_hash = self.hexToBinary(hash)
        return binary_hash.startswith('0'*self.difficulty)