'''
Script for Transaction data structure and other utility functions.
'''
# ==================== Imports ==================== #
from hashlib import sha256
import logging
from collections import Counter 

# ==================== Main ==================== #
logger = logging.getLogger('Transaction')
COINBASE_AMOUNT = 50

class unspentTxOut:
    def __init__(self, txOutId, txOutIndex, address, amount):
        self.txOutId = txOutId
        self.txOutIndex = txOutIndex
        self.address = address
        self.amount = amount

class txOut:
    def __init__(self, address, amnt):
        self.address, self.amount = (address,amnt)

class txIn:
    def __init__(self, txOutId, index, sign):
        self.txOutId, self.txOutIndex, self.signature = (txOutId, index, sign)

class transaction:
    def __init__(self, txId, txIns, txOuts):
        self.txId, self.txIns, self.txOuts = (txId, txIns, txOuts)


def getTransactionId(transxtion):
    
    txInContent = ''
    for i in transxtion.txIns:
        txInContent += i.txOutId + i.txOutIndex
    txOutContent = ''
    for i in transxtion.txOuts:
        txOutContent += i.address + i.amount
    txContent = txInContent + txOutContent
    return(sha256(txContent.encode()).hexdigest())

def validateTransaction(transaction, aUnspentTxOut):
    if(not(isValidTransactionStructure(transaction))):
        return(False)
    
    if(getTransactionId(transaction) != transaction.id):
        logger.error("Invalid Transaction ID: "+ transaction.id)
        return(False)
    
    hasvalidTxIns = reduce(lambda x,y:x and y, list(map(lambda z: validateTxIn(z,transaction,aUnspentTxOut, transaction.txIns))))

    if(not(hasvalidTxIns)):
        logger.error("Some of the Transaction Inputs are Invalid: ", transaction.id)
        return(False)
    
    totalTxInValues = reduce(lambda x,y:x+y, list(map(lambda z:getTxInAmount(z,aUnspentTxOut),transaction.txIns)))

    totalTxOutValues = reduce(lambda x,y:x+y, list(map(lambda z:z.amount),transaction.txOuts))

    if(totalTxInValues != totalTxOutValues):
        logger.error( "totalTxInValues != totalTxOutValues: " + transaction.id)
        return(False)
    
    return(True)


def validateBlockTransaction(aTransactions, aUnspentTxOuts, blockIndex):
    coinBaseTx = aTransactions[0]
    if(not validateCoinbaseTx(coinBaseTx,blockIndex)):
        logger.error("Invalid Coinbase Transaction:" + str(coinBaseTx))
        return(False)
    
    
    flatten=lambda l: sum(map(flatten,l),[]) if isinstance(l,list) else [l]
    txIn = flatten(list(map(lambda x: x.txIns), aTransactions))

    if(hasDuplicates(txIns)):
        return(False)
    

    transactions = aTransactions[1:]
    return(reduce(lambda x,y:x and y, list(map(lambda z: validateTransaction(z,aUnspentTxOuts), transactions)),True))


def validateCoinbaseTx(transaction, blockIndex):
    if(transaction == None):
        logger.error('The first Transaction in the block must be a coinbase Transaction')
        return(False)
    
    if(getTransactionId(transaction) != transaction.id):
        logger.error('Invalid Coinbase Transcation ID: ' + transaction.id)
        return(False)

    if(len(transaction.txIns) != 1):
        logger.error('One txIn must be specified in the coinbase transaction')
        return(False)
    
    if (transaction.txIns[0].txOutIndex != blockIndex):
        logger.error('The txIn signature in coinbase transaction must be the block height')
        return(False)
    
    if (len(transaction.txOuts) != 1):
        logger.error('Invalid number of txOuts in coinbase transaction')
        return(False)
    
    if (transaction.txOuts[0].amount != COINBASE_AMOUNT):
        logger.error('Invalid coinbase amount in coinbase transaction')
        return(False)
    
    return(True)

def hasDuplicates(txIns):
    groups = Counter([i.txOutId + i.txOutIndex for i in txIns])
    for i in groups.keys():
        if(groups[i]>1):
            logger.error("Duplicate Transaction Id: " + i)
            return(True)


        


