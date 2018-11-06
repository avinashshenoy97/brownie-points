'''
Unit tests for the Blockchain module.

Run this script using - nosetests -v --nocapture testTransaction.py
'''

import nose
import os
import sys
import json
import subprocess as sp
from datetime import datetime as dt

sys.path.insert(0, '../../BrowniePoints')

import blockchain
import transaction
import wallet
import transactionPool

testAddress = None
testTransaction = None

def test_initialization():

    ''' Tests whether the wallet is initialised as expected.
    '''
    
    global testAddress

    sp.Popen(['python3', '../../BrowniePoints/rendezvous-server/rendezvous_server.py'])
    blockchain.brownieNet = blockchain.b2b('127.0.0.1', 8000)
    transactionPool.brownieNet = blockchain.brownieNet
    blockchain.init()

    testAddress = wallet.getPublicFromWallet()

    print(testAddress)
    print(wallet.getBalance(testAddress, blockchain.unspentTxOuts))
    assert testAddress is not None

def test_sendTransaction():

    ''' Tests whether sending and receiving of coins happen as expected.
    '''

    global testAddress
    global testTransaction

    print(blockchain.unspentTxOuts)
    
    testTransaction = wallet.sendTransaction(testAddress, 5.0)
    print(testTransaction)
    
    assert testTransaction is not None

def test_validateTransaction():
    
    ''' Tests whether transactions are validated correctly.
    '''
    global testTransaction
    
    response = transaction.validateTransaction(testTransaction, blockchain.unspentTxOuts)
    print(response)

    assert response == True