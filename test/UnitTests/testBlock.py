'''
Unit tests for the Block class.
'''

import nose
import sys
import json
from datetime import datetime as dt

from block import *

testBlock = None

def test_create():

    ''' Tests if the block objects are created as expected and if the __str__ function properly converts a block object to a string
    '''
    
    global testBlock
    
    index = 0
    chash = "7bbf374f987ffc593c6e28a4d558c3a299a9346e98c6448ef4c0c8d248078a36"
    phash = "0000000000"
    timestamp = '2018-11-06 11:00:42.475631'
    data = []
    difficulty = 4
    nonce = 0
    testBlock = block(index, chash, phash, timestamp, data, difficulty, nonce)
    check = OrderedDict([('data', []), ('difficulty', 4), ('hash', '7bbf374f987ffc593c6e28a4d558c3a299a9346e98c6448ef4c0c8d248078a36'), ('index', 0), ('nonce', 0), ('previousHash', '0000000000'), ('timestamp', '2018-11-06 11:00:42.475631')])
    
    assert str(testBlock) == str(check)

def test_deserialize():

    ''' Tests if a dictionary object is properly converted to a block object
    '''

    data = {'difficulty': 4, 'data': [], 'index': 0, 'timestamp': '2018-11-06 11:29:53.532507', 'hash': '7bbf374f987ffc593c6e28a4d558c3a299a9346e98c6448ef4c0c8d248078a36', 'nonce': 0, 'previousHash': '0000000000'}
    newBlock = block.deserialize(data) 
    check = OrderedDict([('data', []), ('difficulty', 4), ('hash', '7bbf374f987ffc593c6e28a4d558c3a299a9346e98c6448ef4c0c8d248078a36'), ('index', 0), ('nonce', 0), ('previousHash', '0000000000'), ('timestamp', dt(2018, 11, 6, 11, 29, 53, 532507))])
    
    assert str(newBlock) == str(check)

def test_calculateHash():

    ''' Tests if a hash calculated for a block is correct
    '''

    global testBlock

    testBlock.data = [{"txId":"21c035da3528874dea1d5b2b7ebe134f8308a29e6b964d8750fc3b79d66f2af7","txIns":[{"signature":"","txOutId":"","txOutIndex":0}],"txOuts":[{"address":"5d06bd4ac9746a9d0b8d02aaac6adc31079b5d96c331432ea324e3156c7f402971d8ad3277367f8838e8707ea83a88ae393fcf227304f43f8ad36463f402df8f","amount":50}]}]
    calculatedHash = testBlock.calculateHash()
    check = "3157a29a9ae598fc3d77897a274b23c1b7e4cee2a6b79ca2b251c8461ce440e3"
    
    assert calculatedHash == check


if __name__ == "__main__":
    nose.main()
