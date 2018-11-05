'''
Unit tests for the brownie-points wallet backend application.
'''
from wallet import *
from transaction import *
from transactionPool import *
from blockchain import *

initWallet("user1")

user1_pub = getPublicFromWallet()
user1_pri = getPrivateFromWallet()

transactionPool = getTransactionPool()

#if user1 mines block1 and gets 50 coins
coin_base = getCoinbaseTransaction(user1_pub, 1)


