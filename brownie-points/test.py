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


trans,usp = getCoinbaseTransaction(user1_pub,0)
unspentTxOuts = [usp]
transa = [trans]
print(unspentTxOuts)

print("Your Current Balance: ", getBalance(user1_pub,unspentTxOuts))

transa.append(createTransaction(user2_pub,10,user1_pri,unspentTxOuts))
print(transa[1].txOuts[0].address)
print(transa[1].txOuts[0].amount)






