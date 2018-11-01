'''
Unit tests for the brownie-points wallet backend application.
'''
from wallet import *
from transaction import *
from transactionPool import *
from blockchain import *
from datetime import datetime as dt

init() #initialize the blockchain

#create a wallet for user1
initWallet("Wallet1")

user1_pub = getPublicFromWallet("Wallet1")
user1_pri = getPrivateFromWallet("Wallet1")

transactionPool = getTransactionPool()

#if user1 mines block1 and gets 50 coins
coin_base = getCoinbaseTransaction(user1_pub, 1)
transactionPool.append(coin_base)

#solving Proof Of Work, validate Transactions create a new block and add to blockchain
block1 = generateNextBlock(transactionPool)

unspentTxOuts = None

#check if user1 got the coinbase amt.
if block1 is not None:
	unspentTxOuts = getUnspentTxOuts()
print("Balance of User1 is: "+str(getBalance(user1_pub,unspentTxOuts)))

#create a wallet for user2
initWallet("Wallet2") #remember now the private key stored in the Wallet folder is changed (not user1's anymore)

user2_pub = getPublicFromWallet("Wallet2")
user2_pri = getPrivateFromWallet("Wallet2")

#sending 40 coins from user1 to user2
transaction1 = createTransaction(user2_pub,40,user1_pri,unspentTxOuts)

#add this transaction1 to transactionPool
addToTransactionPool(transaction1, unspentTxOuts)

#get the transactionPool
transactionPool = getTransactionPool() #it should have only transaction1 in it
print("No. of transactions in Transaction Pool:"+str(len(transactionPool)))

#create a coinbase for block2 - assuming user1 is mining this block
coin_base = getCoinbaseTransaction(user1_pub, 2)

#add coinbase as 1st transaction in transactionPool
transactionPool = [coin_base] + transactionPool

#solving Proof Of Work, validate Transactions create a new block and add to blockchain
block2 = generateNextBlock(transactionPool)

#check if user1 got the coinbase amt. and user2 got 40
if block2 is not None:
	unspentTxOuts = getUnspentTxOuts()
print("Balance of User1 is: "+str(getBalance(user1_pub,unspentTxOuts)))
print("Balance of User2 is: "+str(getBalance(user2_pub,unspentTxOuts)))
