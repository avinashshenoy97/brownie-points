'''
Script for Wallet.
Doubts:
Getting public key from private key
'''
# ==================== Imports ==================== #
#import rainbowKeygen
from ecdsa import SigningKey, SECP256k1
import logging
import os
from transaction import *

# ==================== Main ==================== #
logger = logging.getLogger('Transaction')
folder = "Wallet"


def getPublicFromWallet(keylocn):
	private_key = getPrivateFromWallet(keylocn)
	private_key = SigningKey.from_string(bytes.fromhex(private_key), curve = SECP256k1)
	public_key = private_key.get_verifying_key().to_string().hex()
	return public_key


def getPrivateFromWallet(keylocn):
	if os.path.isfile(folder+"/"+keylocn+"/private.txt"):
		private_key = open(folder+"/"+keylocn+"/private.txt").read()
		return private_key


def generatePrivateKey():
	'''
	generate keys using Quantum resistant keypairs
	myKeyObject = rainbowKeygen()
	myKeyObject.generate_keys() # store keys in folder/wallet/keylocn
	'''

	private_key =  SigningKey.generate(curve = SECP256k1).to_string().hex()
	return private_key


def initWallet(keyloc): #parameter is only for testing
	'''
	check if key exists, if it doesnt then create the keypairs
	'''
	if(os.path.isdir(keyloc) == False):
		os.makedirs(folder+"/"+keyloc, exist_ok=True)
	if os.path.isfile(folder+"/"+keyloc+"/private.txt"):
		return
	else:
		open(folder+"/"+keyloc+"/private.txt","w").write(generatePrivateKey())


def getBalance(address, unspentTxOut):
	balance = 0
	for i in unspentTxOut:
		if(i.address==address):
			balance += i.amount
	return balance


def findTxOutsforAmount(amount, myUnspentTxOuts):
	currentAmount = 0
	includedUnspentTxOuts = []
	for myUnspentTxOut in myUnspentTxOuts:
		includedUnspentTxOuts.append(myUnspentTxOut)
		currentAmount += myUnspentTxOut.amount
		if(currentAmount >= amount):
			leftOverAmount = currentAmount - amount
			return includedUnspentTxOuts,leftOverAmount

	raise Exception("not enough coins to send transaction")


def createTxOuts(receiver_address, myaddress, amount, leftover_amount):
	receiver_Tx = TxOut(receiver_address,amount)
	if(leftover_amount==0):
		return [receiver_Tx]
	
	else:
		leftover_Tx = TxOut(myaddress, leftover_amount)
		return [receiver_Tx,leftover_Tx]
	

def toUnsignedTxIn(unspentTxOut):
	trans_In =TxIn(unspentTxOut.txOutId,unspentTxOut.txOutIndex,None)
	return trans_In
	

def createTransaction(receiver_address, amount, private_key, unspentTxOuts):
	'''
	obtain pub key from private key	
	'''
	myaddress = getPublicKey(private_key)
	myUnspentTxOuts = []	
	for i in unspentTxOuts:
		if(i.address==myaddress):
			myUnspentTxOuts.append(i)

	includedUnspentTxOuts, leftOverAmount =  findTxOutsforAmount(amount, myUnspentTxOuts)
	
	#print("unspent:",includedUnspentTxOuts[0].txOutId)
	unsignedTxIns = []
	for i in includedUnspentTxOuts:
		unsignedTxIns.append(toUnsignedTxIn(i))

	txOuts = createTxOuts(receiver_address, myaddress, amount, leftOverAmount)

	tx = Transaction('',unsignedTxIns,txOuts)
	tx.txId = getTransactionId(tx)
	
	index = 0
	for txIn in tx.txIns:
		txIn.signature = signTxIn(tx,index,private_key,unspentTxOuts)
		index += 1

	return tx
