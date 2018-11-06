'''
Unit tests for the Blockchain module.

Run this script using - nosetests -v --nocapture testBlockchain.py
'''

import nose
import sys
import json
import subprocess as sp
from datetime import datetime as dt

sys.path.insert(0, '../../BrowniePoints')

import blockchain
import transactionPool

def test_initialization():

    ''' Tests the functioning of blockchain initialization, getBlockchain and getLatestBlock.
    '''

    sp.Popen(['python3', '../../BrowniePoints/rendezvous-server/rendezvous_server.py'])
    blockchain.brownieNet = blockchain.b2b('127.0.0.1', 8000)
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