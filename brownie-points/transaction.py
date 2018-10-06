'''
Script for Transaction data structure and other utility functions.
Doubts : Signature (function prototype)
Functions Implemented:

getTransactionId - D
validateTransaction - D 
validateBlockTransactions - D
hasDuplicates - D
validateCoinbaseTx - D
validateTxIn - D
getTxInAmount - D
findUnspentTxOut - D
getCoinbaseTransaction - D
signTxIn - D
updateUnspentTxOuts - D
processTransactions -D
toHexString - D
isValidTxInStructure -D
isValidTxOutStructure -D
isValidTransactionStructure -D
isValidAddress - D

'''
# ==================== Imports ==================== #
from hashlib import sha256
import ecdsa
import logging
#import rainbowKeygen
from collections import Counter
from functools import reduce
import re

# ==================== Main ==================== #
logger = logging.getLogger('Transaction')
COINBASE_AMOUNT = 50

class UnspentTxOut:
    def __init__(self, txOutId, txOutIndex, address, amount):
        self.txOutId = txOutId
        self.txOutIndex = txOutIndex
        self.address = address
        self.amount = amount

class TxOut:
    def __init__(self, address, amnt):
        self.address, self.amount = (address,amnt)

class TxIn:
    def __init__(self, txOutId, index, sign):
        self.txOutId, self.txOutIndex, self.signature = (txOutId, index, sign)

class Transaction:
    def __init__(self, txId, txIns, txOuts):
        self.txId, self.txIns, self.txOuts = (txId, txIns, txOuts)


def getTransactionId(transaction):
    
    txInContent = ''
    for i in transxtion.txIns:
        txInContent += i.txOutId + i.txOutIndex
    txOutContent = ''
    for i in transaction.txOuts:
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



def validateTxIn(txIn, transaction, aUnspentTxOuts):

    referencedUTxOut = None
    for uTxO in aUnspentTxOuts:
        if(uTxO.txOutId == txIn.txOutId and uTxO.txOutIndex == txIn.txOutIndex):
            referencedUTxOut = uTxO
        
        if(referencedUTxOut == None):
            logger.error("Referenced TxOut Not found: " + str(txIn.__dict__))
            return(False)

        addr = referencedUTxOut.address

        vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(addr), curve=ecdsa.SECP256k1)
        if(not vk.verify(bytes.fromhex(txIn.signature), transaction.id)):
            logger.error("Invalid TxIn Signature: " + txIn.signature + "txId: " + transaction.id + "address: " + addr)
            return(False)
        
        return(True)


def getTxInAmount(txIn, aUnspentTxOuts):
    return(findUnspentTxOut(txIn.txOutId, txIn.txOutIndex, aUnspentTxOuts).amount)


def findUnspentTxOut(transactionId, index, aUnspentTxOuts):
    for uTxO in aUnspentTxOuts:
        if(uTxO.txOutId == transactionId and uTxO.txOutIndex == index):
            return(uTxO)
    
    return(None)

def getCoinbaseTransaction(address, blockIndex):
    t = Transaction()
    txIn = TxIn()
    txIn.signature = ''
    txIn.txOutId = ''
    txIn.txOutIndex = blockIndex

    t.txIns = [txIn]
    t.txOuts = [TxOut(address, COINBASE_AMOUNT)]
    t.id = getTransactionId(t);
    return(t)


def signTxIn(tx,txInIndex,private_key,UnspentTxOuts):
	txIn = tx.txIns[txInIndex]
	datatosign = tx.txId
	referencedUnspentTxOut = findUnspentTxOut(txIn.txOutId, txIn.txOutIndex, UnspentTxOuts);

	if(referencedUnspentTxOut is None):
		logger.error("could not find referenced txOut while creating transaction")
		raise Exception("could not find referenced txOut while creating transaction")

	referencedAddress = referencedUnspentTxOut.address
    
	
	'''
	obtain pub key from priv key
	'''
	if(getPublicKey() != referencedAddress):
		logger.error('Signing an input whose address doesnt match with that present in txIn')
		raise Exception('Signing an input whose address doesnt match with that present in txIn')
	
	'''
	?????????Doubts : Signature (function prototype)?????????
	#signature = rainbowKeygen.sign(private_key, datatosign)
	'''

	private_key = SigningKey.from_string(bytes.fromhex(private_key))
	signature = private_key.sign(datatosign.encode())

	return str(signature)


def updateUnspentTxOuts(aTransactions, aUnspentTxOuts):
	newUnspentTxOuts = []
	for t in aTransactions:
		for txOut,index in enumerate(t.txOuts):
			newUnspentTxOuts = UnspentTxOut(t.id, index, txOut.address,txOut.amount)
	newUnspentTxOuts = reduce(lambda a,b : a + b, newUnspentTxOuts, [])
	consumedTxOuts = map(lambda txIn : UnspentTxOut(txIn.txOutId, txIn.txOutIndex, '',0), reduce(lambda a,b : a + b, [ t.txIns for t in aTransactions], []))
	resultingUnspentTxOuts = filter(lambda uTxO : findUnspentTxOut(uTxO.txOutId, uTxO.txOutIndex, consumedTxOuts) == False, aUnspentTxOuts) + newUnspentTxOuts
	return resultingUnspentTxOuts


def processTransactions(aTransactions, aUnspentTxOuts, blockIndex):
    if(not validateBlockTransaction(aTransactions, aUnspentTxOuts, blockIndex)):
        logger.error("Invalid Block Transaction")
        return(None)
    
    return(updateUnspentTxOuts(aTransactions, aUnspentTxOuts))

'''
const toHexString = (byteArray): string => {
    return Array.from(byteArray, (byte: any) => {
        return ('0' + (byte & 0xFF).toString(16)).slice(-2);
    }).join('');
};
'''
#not sure why they are taking byte by byte in the byteArray string?
def toHexString(byteArray):
	return reduce(lambda a, b : a + b,map(lambda byte: '0' + (hex(int(byte) & 0xFF)[2:])[-2:], [byte for byte in byteArray]))
			
def getPublicKey(private_key):
	private_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key))
	public_key = private_key.get_verifying_key().to_string().hex()
	return public_key

def isValidTxInStructure(txIn):
	if(txIn is None):
		logger.error("txIn is null")
		return False
	elif(type(txIn.signature) is not str):
		logger.error('invalid signature type in txIn')
		return False
	elif(type(txIn.txOutId) is not str):
		logger.error('invalid txOutId in txIn')
		return False
	elif(not((type(txIn.signature) is int) or (type(txIn.signature) is long))):
		logger.error('invalid txOutIndex type in txIn')
		return False
	else:
		return True


def isValidTxOutStructure(txOut):
	if(txOut is None):
		logger.error("txOut is null")
		return False
	elif(type(txOut.address) is not str):
		logger.error('invalid address type in txOut')
		return False
	elif(not(isValidAddress(txOut.address)):
		logger.error('invalid txOut address in txOut')
		return False
	elif(not((type(txOut.amount) is int) or (type(txOut.amount) is long))):
		logger.error('invalid tamount type in txOut')
		return False
	else:
		return True

def isValidTransactionsStructure(transactions):
	for transaction in transactions:
		valid = isValidTransactionStructure(transaction)
		if(not valid):
			return False
	return True

def isValidTransactionStructure(transaction):
	if(type(transaction.txId) is not str):
		logger.error("transactionId missing")
		return False
	if(type(transaction.txIns) is not list):
		logger.error("invalid txIns type in transaction")
		return False
	for txin in transaction.txIns:
		valid = isValidTxInStructure(txin)
		if(not valid):
			return False
	if(type(transaction.txOuts) is not list):
		logger.error("invalid txOuts type in transaction")
		return False
	for txout in transaction.txOuts:
		valid = isValidTxOutStructure(txout)
		if(not valid):
			return False
	return True

#valid address is a valid ecdsa public key in the 04 + X-coordinate + Y-coordinate format
def isValidAddress(address):
	if len(address) != 130:
		logger.error(address)
		logger.error('invalid public key length')
		return False
	p = re.compile('^[a-fA-F0-9]+$')
	if p.match(address) is None:
		logger.error('public key must contain only hex characters')
		return False
	if address[:2] == '04':
		logger.error('public key must start with 04')
		return False
	return True
