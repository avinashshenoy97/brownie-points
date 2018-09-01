'''
Script for Block data structure and its properties.
'''
# ==================== Imports ==================== #
from hashlib import sha256
from datetime import datetime as dt


# ==================== Main ==================== #
class block:

    def __init__(self, index, hash, previousHash, timestamp, data):
        self.index, self.hash, self.previousHash, self.timestamp, self.data = (index, hash, previousHash, timestamp, data)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def calculateHash(index, previousHash, timestamp, data):
        '''Calculates a block's hash, given its index, the previous block's hash, its timestamp, and its data.

        Arguments:
            index: the block's index.

            previousHash: the hash of the block behind the given block in the chain.

            timestamp: the timestamp of the block.

            data: the data of the block.

        Returns:
            The hash string (in hexadecimals) of the given data.
        '''
        preHashedString = str(index) + previousHash + str(timestamp) + data
        return sha256(bytes(preHashedString, 'utf-8')).hexdigest()

    def generateNextBlock(self, blockData):
        '''Given the block data, generates the subsequent block in the blockchain.

        Arguments:
            blockData: the data of the new block.

        Returns:
            The new block generated with the given data and appropriate metadata.
        '''
        nextIndex = self.index + 1
        nextTimestamp = dt.now()
        nextHash = block.calculateHash(nextIndex, self.hash, nextTimestamp, blockData)

        return block(nextIndex, nextHash, self.hash, nextTimestamp, blockData)
