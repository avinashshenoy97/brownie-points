from transaction import transaction, txIn, unspentTxOut, validateTransaction
from copy import deepcopy
from functools import reduce
import logging

logger = logging.getLogger("TransactionPool")

transactionPool = []

def getTransactionPool():
	return deepcopy(transactionPool)


def addToTransactionPool(tx, unspentTxOuts):
	if(validateTransaction(tx, unspentTxOuts) == False):
		raise Exception("Trying to add invalid tx to pool")

	if(isValidTxForPool(tx, transactionPool) == False):
		raise Exception("Trying to add invalid tx to pool")

	logger.info("Adding to tx pool : " + str(tx.txId)) #JSON.stringify(tx)??

	transactionPool.append(tx)


def hasTxIn(txIn, unspentTxOuts):
	foundTxIn = None

	for uTxO in unspentTxOuts:
		foundTxIn = (uTxO.txOutId == txIn.txOutId and uTxO.txOutIndex == txIn.txOutIndex)

	return (foundTxIn is not None)


def updateTransactionPool(unspentTxOuts):
	invalidTxs = []
	
	for tx in transactionPool:
		for txIn in tx.txIns:
			if(hasTxIn(txIn, unspentTxOuts) == False):
				invalidTxs.append(tx)
				break
	
	if(len(invalidTxs) > 0):
		logger.error("removing the following transactions from txPool:" + reduce(lambda a,b : str(a.txId) + ',' + str(b.txId), invalidTxs))
		transactionPool = [ tx for tx in transactionPool if tx not in invalidTxs]


def getTxPoolIns(aTransactionPool):
	return [tx.txIns for tx in aTransactionPool]  #.value() in lodash??


def isValidTxForPool(tx, aTtransactionPool):
	txPoolIns = getTxPoolIns(aTtransactionPool)

	def containsTxIn(txIn):
		for txPoolIn in txPoolIns:
			if txIn.txOutIndex == txPoolIn.txOutIndex and txIn.txOutId == txPoolIn.txOutId:
				return True
		return False

	for txIn in tx.txIns:
		if(containsTxIn(txPoolIns, txIn) == True):
			logger.info("txIn already found in the txPool")
			return False
	return True
