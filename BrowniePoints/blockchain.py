'''
Script for blockchain helper functions.
'''
# ==================== Imports ==================== #
import logging
from datetime import datetime as dt

from block import block
from b2b import *


# ==================== Globals ==================== #
logger = logging.getLogger('Blockchain')
genesisBrownie = None
brownieChain = None
browniePeers = []
difficulty = 4
BLOCK_GENERATION_INTERVAL = 10 # in seconds
DIFFICULTY_ADJUSTMENT_INTERVAL = 10 # in blocks

def init():
    global genesisBrownie
    global brownieChain
    global difficulty
    genesisBrownie = block(0, '7bbf374f987ffc593c6e28a4d558c3a299a9346e98c6448ef4c0c8d248078a36', None, dt.now(), 'the holy brownie', difficulty, 0)
    brownieChain = [genesisBrownie]


# ==================== Main ==================== #

def getBlockchain():
    ''' Returns: The chain stored on the node.
    '''
    global brownieChain
    return brownieChain

def getLatestBlock():
    ''' Returns: The latest block that was added to the chain on the node.
    '''
    global brownieChain
    return brownieChain[-1]

def generateNextBlock(blockData):
    '''Given the block data, generates the subsequent block in the blockchain.

    Arguments:
        blockData: the data of the new block.

    Returns:
        The new block generated with the given data and appropriate metadata.
    '''
    latestBlock = brownieChain[-1]
    nextIndex = latestBlock.index + 1
    nextTimestamp = dt.now()
    nextHash = block.calculateHash(nextIndex, latestBlock.hash, nextTimestamp, blockData, 0)

    return block(nextIndex, nextHash, latestBlock.hash, nextTimestamp, blockData, difficulty, 0)


def isValidBlock(newBlock, previousBlock):
    '''Checks and returns whether the new block generated is valid with respect to its previous block in the blockchain.

    Arguments:
        newBlock: the newly generated block or the block to be tested.

        previousBlock: the block prior to the new block in the blockchain.

    Returns:
        Boolean True/False
    '''
    if newBlock.index != (previousBlock.index + 1):
        logger.error('New block index: ' + str(newBlock.index) + ' is invalid after: ' + str(previousBlock.index))
        return False

    if newBlock.previousHash != previousBlock.hash:
        logger.error('New block hash at: ' + str(newBlock.index) + ' is invalid after: ' + str(previousBlock.index))
        return False

    if newBlock.hash != block.calculateHash(newBlock.index, newBlock.previousHash, newBlock.timestamp, newBlock.data, newBlock.nonce):
        logger.error('New block hash at: ' + str(newBlock.index) + ' is invalid...calculated hash does not match block\'s hash.')
        return False

    return True


def isValidBlockStructure(testBlock):
    '''Checks and returns whether a block's structure is in line with the design for a standard block in the blockchain.

    Arguments:
        testBlock: the block to be tested.

    Returns:
        Boolean True/False
    '''
    if type(testBlock.index) != int:
        logger.error('Invalid type of index: ' + str(type(testBlock.index)) + ' at index is ' + str(testBlock.index))
        return False

    if type(testBlock.hash) != str:
        logger.error('Invalid type of hash: ' + str(type(testBlock.hash)) + ' at index is ' + str(testBlock.index))
        return False

    if type(testBlock.previousHash) != int:
        logger.error('Invalid type of previous hash: ' + str(type(testBlock.previousHash)) + ' at index is ' + str(testBlock.index))
        return False
    
    if type(testBlock.timestamp) != dt:
        logger.error('Invalid type of timestamp: ' + str(type(testBlock.timestamp)) + ' at index is ' + str(testBlock.index))
        return False

    if type(testBlock.data) != str:
        logger.error('Invalid type of data: ' + str(type(testBlock.data)) + ' at index is ' + str(testBlock.index))
        return False

    return True


def isValidChain(testChain, genesisBlock):
    '''Checks and returns whether the given blockchain is a valid chain of blocks.

    Arguments:
        testChain: the chain of blocks to be tested.

        genesisBlock: the first block generated by the admin of the blockchain.

    Returns:
        Boolean True/False
    '''
    if testChain[0] != genesisBlock:
        logger.error('Invalid block chain, genesis block does not match.')
        return False

    for b in range(1, len(testChain)):
        if not isValidBlock(testChain[b], testChain[b - 1]):
            logger.error('Block chain inconsistent at index: ' + str(b))
            return False

    return True


def replaceChain(newChain):
    '''Replaces the node's copy of the blockchain with the given chain if it is valid and longer.

    Arguments:
        newChain: the new chain to replace the existing blockchain.
    '''
    global brownieChain
    if isValidChain(newChain, genesisBrownie):
        if len(newChain) > len(brownieChain):
            logger.info('Replacing chain.')
            brownieChain = newChain
            # broadcastLatest()
            broadcastFullChain()
        else:
            logger.info('Received chain is not longer. Discarding.')
    else:
        logger.info('Received invalid chain. Discarding.')


def connectToPeer(peer):
    '''Connects to another peer on the brownie p2p network.
    '''
    browniePeers.append(peer)
    return

def broadcastFullChain():
    global brownieNet
    msg = {'msg_type': 'response_blockchain', 'payload': json.dumps(getBlockchain(), cls=blockEncoder)}
    brownieNet.broadcast(msg)

def getDifficulty(brownieChain):
    '''

    :param brownieChain:
    :return:
    '''
    latestBlock = brownieChain[-1]

    if latestBlock.index % DIFFICULTY_ADJUSTMENT_INTERVAL == 0 and latestBlock.index != 0:
        return getAdjustedDifficulty(latestBlock, brownieChain)

    return latestBlock.difficulty

def getAdjustedDifficulty(latestBlock, brownieChain):
    '''

    :param latestBlock:
    :param brownieChain:
    :return:
    '''
    prevAdjustmentBlock =  brownieChain[ -DIFFICULTY_ADJUSTMENT_INTERVAL]
    timeExpected =  BLOCK_GENERATION_INTERVAL * DIFFICULTY_ADJUSTMENT_INTERVAL
    timeTaken = latestBlock.timestamp - prevAdjustmentBlock.timestamp

    if timeTaken < timeExpected / 2 :
       return prevAdjustmentBlock.difficulty + 1
    elif timeTaken > timeExpected * 2 :
        return prevAdjustmentBlock.difficulty - 1

    return prevAdjustmentBlock.difficulty

def isValidTimestamp(newBlock, previousBlock):
    '''

    :param newBlock:
    :param previousBlock:
    :return:
    '''
    return  previousBlock.timestamp - 60 < newBlock.timestamp and newBlock.timestamp - 60 < dt.now()