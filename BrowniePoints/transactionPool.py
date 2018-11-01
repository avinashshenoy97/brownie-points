'''
Script incharge of maintaining the transaction pool.
'''
# ==================== Imports ==================== #
from copy import deepcopy
from functools import reduce
import json
import logging

from transaction import Transaction, TxIn, UnspentTxOut, validateTransaction


# ==================== Globals ==================== #
transactionPool = []
logger = logging.getLogger("Transaction")


# ==================== Main ==================== #

def getTransactionPool():
	global transactionPool
	return deepcopy(transactionPool)


def broadcastFullTransactionPool():
	global transactionPool
	global brownieNet
	msg = {'msg_type': 'response_transaction_pool', 'payload': json.dumps(transactionPool)}
	brownieNet.broadcast(msg)


def addToTransactionPool(tx, UnspentTxOut):
	if(validateTransaction(tx, UnspentTxOut) == False):
		raise Exception("Trying to add invalid tx to pool")

	if(isValidTxForPool(tx, transactionPool) == False):
		raise Exception("Trying to add invalid tx to pool")

	logger.info("Adding to tx pool : " + str(tx.txId)) #JSON.stringify(tx)??

	transactionPool.append(tx)
	broadcastFullTransactionPool()


def hasTxIn(TxIn, UnspentTxOut):
	foundTxIn = None

	for uTxO in UnspentTxOut:
		foundTxIn = (uTxO.txOutId == TxIn.txOutId and uTxO.txOutIndex == TxIn.txOutIndex)

	return (foundTxIn is not None)


def updateTransactionPool(UnspentTxOut):
	global transactionPool
	invalidTxs = []
	
	for tx in transactionPool:
		for txIn in tx.txIns:
			if(hasTxIn(txIn, UnspentTxOut) == False):
				invalidTxs.append(tx)
				break
	
	if(len(invalidTxs) > 0):
		logger.error("Removing the following transactions from txPool:" + reduce(lambda a,b : str(a.txId) + ',' + str(b.txId), invalidTxs))
		transactionPool = [ tx for tx in transactionPool if tx not in invalidTxs]
		broadcastFullTransactionPool()


def getTxPoolIns(aTransactionPool):
	return [tx.txIns for tx in aTransactionPool]  #.value() in lodash??


def isValidTxForPool(tx, aTtransactionPool):
	txPoolIns = getTxPoolIns(aTtransactionPool)

	def containsTxIn(TxIn):
		for txPoolIn in txPoolIns:
			if TxIn.txOutIndex == txPoolIn.txOutIndex and TxIn.txOutId == txPoolIn.txOutId:
				return True
		return False

	for txIn in tx.txIns:
		if(containsTxIn(txIn) == True):
			logger.info("txIn already found in the txPool")
			return False
	return True