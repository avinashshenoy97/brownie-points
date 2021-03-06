'''
Script for blockchain helper functions.
'''
# ==================== Imports ==================== #
import logging
from datetime import datetime as dt
from copy import deepcopy

import transaction
import transactionPool
import wallet
from block import block, customEncoder
from b2b import *


# ==================== Globals ==================== #
logger = logging.getLogger('Blockchain')
genesisBrownie = None
brownieChain = []
browniePeers = []
unspentTxOuts = []
difficulty = 4
BLOCK_GENERATION_INTERVAL = 10 # in seconds
DIFFICULTY_ADJUSTMENT_INTERVAL = 10 # in blocks

def init():
	global genesisBrownie
	global brownieChain
	global difficulty
	global unspentTxOuts
	wallet.initWallet()
	random_user = wallet.getPublicFromWallet()
	genesisBrownie = block(0, '7bbf374f987ffc593c6e28a4d558c3a299a9346e98c6448ef4c0c8d248078a36', '0000000000' , dt.now(), [transaction.getCoinbaseTransaction(random_user, 0)], difficulty, 0)
	brownieChain = [genesisBrownie]
	unspentTxOuts.extend(transaction.processTransactions(genesisBrownie.data, [], 0))


# ==================== Main ==================== #
def getBlockchain():
	''' Returns: The entire blockchain stored on this node.
	'''
	global brownieChain
	return brownieChain


def getUnspentTxOuts():
	'''Returns: A read-only copy of all unspent TxOuts on the blockchain.
	'''
	global unspentTxOuts
	return deepcopy(unspentTxOuts)


def setUnspentTxOuts(newUnspentTxOuts):
	'''Updates the unspentTxOuts.
	'''
	global unspentTxOuts
	global logger
	logger.info('Updating unspenTxOuts')
	unspentTxOuts = newUnspentTxOuts


def getLatestBlock():
	''' Returns: The latest block that was added to the chain on the node.
	'''
	global brownieChain
	return brownieChain[-1]


def generateRawNextBlock(blockData):
	'''Given the block data, generates the subsequent block in the blockchain.

	Arguments:
		blockData: the data of the new block.

	Returns:
		The new block generated with the given data and appropriate metadata.
	'''
	global logger

	latestBlock = brownieChain[-1]
	difficulty = getDifficulty(getBlockchain())
	nextIndex = latestBlock.index + 1
	nextTimestamp = dt.now()
	newBlock = findBlock(nextIndex, latestBlock.hash, nextTimestamp, blockData, difficulty)
	if addBlockToChain(newBlock):
		#broadcastLatest()
		broadcastFullChain()
		return newBlock
	else:
		logger.error('Error adding block to chain!')
		return None


def generateNextBlock():
	'''Generate next block by generating a coinbase transaction for it and adding transactions from the transactionPool.

	Returns:
		The newly generated block.
	'''
	coinbaseTx = transaction.getCoinbaseTransaction(wallet.getPublicFromWallet(), getLatestBlock().index + 1)
	if len(transactionPool.getTransactionPool()) > 0:
		return generateRawNextBlock([coinbaseTx] + transactionPool.getTransactionPool())
	else:
		raise ValueError('TransactionPool is empty!')


def findBlock(index, previousHash, timestamp, data, difficulty):
	'''Creates a new valid block by finding the nonce value such that the created block satisfies current difficulty.

	Arguments:
		index: index of the block
	
		previousHash: hash the block preceding the new block
	
		timestamp: time when the new block is created
	
		data: data
		
		difficulty: current difficulty
	Returns:
		The new block generated with the correct nonce.
	'''
	nonce = 0
	while True:
		hash = calculateHash(index, previousHash, timestamp, data, difficulty, nonce)
		if hashMatchesDifficulty(hash, difficulty):
			return block(index, hash, previousHash, timestamp, data, difficulty, nonce)

		nonce += 1


def addBlockToChain(block):
	global brownieChain
	global unspentTxOuts
	
	if isValidBlock(block, getLatestBlock()) :
		ret = transaction.processTransactions(block.data, unspentTxOuts, block.index)
		if ret is None:
			return False
		else:
			brownieChain.append(block)
			setUnspentTxOuts(ret)
			transactionPool.updateTransactionPool(getUnspentTxOuts())
			return True
	return False


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

	if newBlock.hash != calculateHash(newBlock.index, newBlock.previousHash, newBlock.timestamp, newBlock.data, newBlock.difficulty, newBlock.nonce): #newBlock.calculateHash(preHash=True):
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

	'''if type(testBlock.data) != str:
		logger.error('Invalid type of data: ' + str(type(testBlock.data)) + ' at index is ' + str(testBlock.index))
		return False'''

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
			
			aUnspentTxOuts = list()
			for b in brownieChain:
				aUnspentTxOuts = transaction.processTransactions(b.data, aUnspentTxOuts, b.index)
				# have to check for null

			setUnspentTxOuts(aUnspentTxOuts)
			transactionPool.updateTransactionPool(unspentTxOuts)
			# broadcastLatest()
			broadcastFullChain()
		else:
			logger.info('Received chain is not longer. Discarding.')
	else:
		logger.info('Received invalid chain. Discarding.')

# Redundant function
"""
def connectToPeer(peer):
	'''Connects to another peer on the brownie p2p network.
	'''
	browniePeers.append(peer)
	return
"""


def broadcastFullChain():
	global brownieNet
	msg = {'msg_type': 'response_blockchain', 'payload': json.dumps(getBlockchain(), cls=customEncoder)}
	brownieNet.broadcast(msg)


def broadcastLatest():
	global brownieNet
	msg = {'msg_type': 'response_latest', 'payload': json.dumps(str(getLatestBlock()))}
	brownieNet.broadcast(msg)


def getDifficulty(brownieChain):
	'''Determines and retrieves the difficulty level of the blockchain.

	Arguments:
		brownieChain: the blockchain.

	Returns:
		The difficulty level.
	'''
	latestBlock = brownieChain[-1]

	if latestBlock.index % DIFFICULTY_ADJUSTMENT_INTERVAL == 0 and latestBlock.index != 0:
		return getAdjustedDifficulty(latestBlock, brownieChain)

	return latestBlock.difficulty


def getAdjustedDifficulty(latestBlock, brownieChain):
	'''Gets the adjusted difficulty level of the blockchain.

	Arguments:
		latestBlock: the latest block of the blockchain.

		brownieChain: the blockchain.

	Returns:
		The adjusted difficulty level of the blockchain.
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
	'''Checks if the timestamp of the new block is valid with respect to the timestamp of the previous block.

	Arguments:
		newBlock: the newBlock to be validated.

		previousBlock: the block to reference for validating the timestamp.

	Returns:
		Boolean stating whether newBlock has a valid timestamp or not.
	'''
	return  previousBlock.timestamp - 60 < newBlock.timestamp and newBlock.timestamp - 60 < dt.now()


def hexToBinary(hash_str):
	'''Converts the given input 'hash_str' from hexadecimal to its equivalent binary representation

	:param
		hash_str: hexadecimal string
	:return: string of 256 binary characters, representing the binary value of the hash
	'''
	return bin(int(hash_str, 16))[2:].zfill(256)    


def hashMatchesDifficulty(hash, difficulty):
	'''Checks if the given hash matches the current difficulty level

	Arguments:
		hash: bit string representing binary value of the hash
		
		difficulty: current difficulty level of the network
	
	Returns: 
		A boolean indicating whether the hash matches the difficulty or not.
	'''
	binary_hash = hexToBinary(hash)
	return binary_hash.startswith('0' * difficulty)


def calculateHash(index, previousHash, timestamp, data, difficulty, nonce):
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
	_data = list()
	for d in data:
		_data.append(str(d))
	preHashedString = str(index) + previousHash + str(timestamp) + str(_data) + str(difficulty) + str(nonce)
	logger.debug('PREHASHED: ' + preHashedString)
	return sha256(bytes(preHashedString, 'utf-8')).hexdigest()
