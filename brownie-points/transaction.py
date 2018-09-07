'''
Script for Transaction data structure and other utility functions.
'''
# ==================== Imports ==================== #
from hashlib import sha256
import logging

# ==================== Main ==================== #
logger = logging.getLogger('Transaction')
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

def validateTransactionStructure(transaction, aUnspentTxOut):
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









        


