'''
Unit tests for the Blockchain module.
'''

import nose
import sys
import json
import subprocess as sp
from datetime import datetime as dt

import blockchain
import transactionPool

def test_initialization():

    ''' Tests the functioning of blockchain initialization, getBlockchain and getLatestBlock.
    '''

    transactionPool.brownieNet = blockchain.brownieNet
    blockchain.init()

    print(blockchain.getBlockchain())

    print(blockchain.getLatestBlock())

    print(blockchain.genesisBrownie)

    assert str(blockchain.getLatestBlock()) == str(blockchain.genesisBrownie)
    assert str(blockchain.getBlockchain()[-1]) == str(blockchain.genesisBrownie)    

def test_generateNextBlock():

    ''' Tests whether findBlock, addBlockToChain, generateRawNextBlock and generateNextBlock are functioning as expected.
    '''

    newBlock = blockchain.generateNextBlock()
    assert newBlock is not None

if __name__ == "__main__":
    nose.main()