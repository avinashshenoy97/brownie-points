'''
Script for Wallet.
Doubts:
Getting public key from private key
'''
# ==================== Imports ==================== #
from CryptoVinaigrette.Generators import rainbowKeygen
from ecdsa import SigningKey, SECP256k1
import logging
import os
from transaction import *
import dill


# ==================== Globals ==================== #
walletLogger = logging.getLogger('Brownie-Wallet')
__privKeyFile__ = 'rPriv.rkey'
__pubKeyFile__ = 'rPub.rkey'
keylocn = "Wallet"


# ==================== Main ==================== #
class brownieWallet:
	def __init__(self):
		'''Initialise brownie wallet with private and public keys. Generates keys if they do not exist already.'''
		if os.path.exists(__privKeyFile__) and os.path.exists(__pubKeyFile__):
			self.privKey = dill.load(__privKeyFile__)
			self.pubKey = dill.load(__pubKeyFile__)
		else:
			keyGen = rainbowKeygen()
			self.privKey = keyGen.generate_privatekey(both=True, save=True)
			self.pubKey = self.privKey.pubKey

	def getPublicFromWallet(self):
		'''Returns the public key for quantum resistant cryptographic signature verification.'''
		return self.pubKey

	def getPrivateFromWallet(self):
		'''Returns the private key for quantum resistant cryptographic signing.'''
		return self.privKey

	def getBalance(self, address, unspentTxOut):
		'''Returns the wallet balance of a given address, given the unspect transaction output objects.
		
		Arguments:
			address: the wallet address whose balance to retrieve
			
			unspectTxOut: the unspect transaction output objects using which, the wallet balance is to be calculated.
			
		Returns:
			The wallet balance in brownie-points.
		'''
		return sum([float(i.amount) for i in unspectTxOut if i.address == address])
		# balance = 0
		# for i in unspentTxOut:
		# 	if(i.address == address):
		# 		balance += i.amount
		# return balance

	def findTxOutsforAmount(self, amount, myUnspentTxOuts):
		currentAmount = 0
		includedUnspentTxOuts = []
		for myUnspentTxOut in myUnspentTxOuts:
			includedUnspentTxOuts.append(myUnspentTxOut)
			currentAmount += myUnspentTxOut.amount
			if(currentAmount >= amount):
				leftOverAmount = currentAmount - amount
				return (includedUnspentTxOuts, leftOverAmount)

		raise Exception("Not enough coins to send transaction")

	def createTxOuts(self, receiver_address, myaddress, amount, leftover_amount):
		receiver_Tx = TxOut(receiver_address,a mount)
		if(leftover_amount==0):
			return [receiver_Tx]
		
		else:
			leftover_Tx = TxOut(myaddress, leftover_amount)
			return [receiver_Tx,leftover_Tx]
		
	def toUnsignedTxIn(self, unspentTxOut):
		trans_In = TxIn(unspentTxOut.txOutId, unspentTxOut.txOutIndex, None)
		return trans_In
		
	def createTransaction(self, receiver_address, amount, private_key, unspentTxOuts):
		'''
		obtain pub key from private key	
		'''
		myaddress = getPublicKey(private_key)
		myUnspentTxOuts = []	
		for i in unspentTxOuts:
			if(i.address == myaddress):
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
