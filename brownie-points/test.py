from transaction import *
from wallet import *
from transactionPool import *


initWallet()
initWallet2()

user1_pub = getPublicFromWallet()
user2_pub = getPublicFromWallet2()

user1_pri = getPrivateFromWallet()
user2_pri = getPrivateFromWallet2()

print(user1_pub)
print(user2_pub)

unspentTxOuts = []

print("***********************1**************************")
coin = getCoinbaseTransaction(user1_pub,0)
transa = [coin]
#print(unspentTxOuts)
unspentTxOuts = processTransactions(transa, unspentTxOuts, 0)
print("A Balance: ", getBalance(user1_pub,unspentTxOuts))
print("B Balance: ", getBalance(user2_pub,unspentTxOuts))

print("***********************2**************************")
coin = getCoinbaseTransaction(user2_pub,1)
transa = [coin]
#print(unspentTxOuts)
unspentTxOuts = processTransactions(transa, unspentTxOuts,1)
print("A Balance: ", getBalance(user1_pub,unspentTxOuts))
print("B Balance: ", getBalance(user2_pub,unspentTxOuts))


print("*********************3****************************")

coin = getCoinbaseTransaction(user1_pub,2)
transa = [coin]
transa.append(createTransaction(user2_pub,40,user1_pri,unspentTxOuts))
transa.append(createTransaction(user1_pub,30,user2_pri,unspentTxOuts))
unspentTxOuts = processTransactions(transa, unspentTxOuts, 2)
print("A Balance: ", getBalance(user1_pub,unspentTxOuts))
print("B's Balance: ", getBalance(user2_pub,unspentTxOuts))


'''
print("***********************3**************************")
coin = getCoinbaseTransaction(user1_pub,2)
transa = [coin]
transa.append(createTransaction(user1_pub,5,user2_pri,unspentTxOuts))
unspentTxOuts = processTransactions(transa, unspentTxOuts, 2)

print("A Balance: ", getBalance(user1_pub,unspentTxOuts))

print("B's Balance: ", getBalance(user2_pub,unspentTxOuts))


print("***********************4***************************")
coin = getCoinbaseTransaction(user1_pub,3)
transa = [coin]
transa.append(createTransaction(user1_pub,5,user2_pri,unspentTxOuts))
unspentTxOuts = processTransactions(transa, unspentTxOuts, 3)

print("A Balance: ", getBalance(user1_pub,unspentTxOuts))

print("B's Balance: ", getBalance(user2_pub,unspentTxOuts))



print("***********************5**************************")
coin = getCoinbaseTransaction(user2_pub,4)
transa = [coin]
transa.append(createTransaction(user2_pub,10,user1_pri,unspentTxOuts))
unspentTxOuts = processTransactions(transa, unspentTxOuts, 4)
print("A Balance: ", getBalance(user1_pub,unspentTxOuts))

print("B's Balance: ", getBalance(user2_pub,unspentTxOuts))
'''
