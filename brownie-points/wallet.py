'''
Script for Wallet.
Doubts:
Getting public key from private key
'''
# ==================== Imports ==================== #
import rainbowKeygen
import logging
import os
from transactions import *

# ==================== Main ==================== #
logger = logging.getLogger('Transaction')
private_keylocn = "/Wallet/private_key"
public_keylocn = "/Wallet/public_key"

'''
???????Below two functions and function to obtain public key from private????
'''
def getPublicKey():
	if os.path.isfile(public_keylocn):
		f = open(public_keylocn,"r")
		pub_key = f.readline()
		return pub_key

def getPrivateKey():
	if os.path.isfile(private_keylocn):
		f = open(private_keylocn,"r")
		private_key = f.readline()
		return private_key

def generate_keypairs():
	'''
	generate keys using Quantum resistant keypairs
	'''
	myKeyObject = rainbowKeygen()
	myKeyObject.generate_keys() # store keys in folder/wallet/keylocn

def initWallet(): 
	'''
	check if key exists, if it doesnt then create the keypairs
	'''
	if os.path.isfile(private_keylocn) and os.path.isfile(public_keylocn):
		return
	else:
		generate_keypairs()

def getBalance(address,unspentTxOut):
	balance = 0
	for i in unspentTxOut:
		if(i.address==address):
			balance += i.amount
	return balance

	
def findTxOutsforAmount(amount,myUnspentTxOuts):
	currentAmount = 0
	includedUnspentTxOuts = []
	for myUnspentTxOut in myUnspentTxOuts:
		includedUnsoentTxOuts.append(myUnspentTxOut)
		currentAmount += myUnspentTxOut.amount
		if(currentAmount >= amount):
			leftoverAmount = currentAmount - amount
			return includedUnspentTxOuts,leftOverAmount

	raise Exception("not enough coins to send transaction")

def createTxOuts(receiver_address,myaddress,amount,leftover_amount):
	receiver_Tx = TxOut(receiver_address,amount)
	if(leftover_amount==0):
		return [receiver_Tx]
	
	else:
		leftover_Tx = TxOut(myaddress,leftover_amount)
		return [receiver_Tx,leftover_Tx]
	
def toUnsignedTxIn(unspentTxOut):
	trans_In = txIn(unspentTxOut.txOutId,unspentTxOut.txOutIndex,unspentTxOut.signature)
	return trans_In
	
def createTransaction(receiver_address,amount,private_key,unspentTxOuts):
	'''
	obtain pub key from private key	
	'''
	myaddress = getPublicKey()
	myUnspentTxOuts = []	
	for i in unspentTxOuts:
		if(i.address==myaddress):
			myUnspentTxOuts.append(i)

	includedUnspentTxOuts, leftOverAmount = findTxOutsForAmount(amount, myUnspentTxOuts)

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

	return txIn
