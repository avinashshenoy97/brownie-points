from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import requests

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
main_dir = os.path.dirname(parentdir)
sys.path.insert(0,main_dir)
print(sys.path)

# from browniePoints import wallet as w
# from browniePoints import transaction as t
# Create your views here.
context={}
myAddress=''
# publicAddr=w.getPublicFromWallet()
# unspentTxOut=[]
# transactions=[]
# transactionAddr=[]
# transactionCoins=[]

# w.initWallet()
# trans,usp = t.getCoinbaseTransaction(publicAddr,0)
# unspentTxOut.append(usp)
# transactions.append(trans)
def wallet(request):
	return render(request, "index.html",context)

class sendCoinsView(APIView):
	def put(self,request):
		# global unspentTxOut
		print("put",request.data)
		# tra = w.createTransaction(request.data['address'],request.data['coinCount'],w.getPrivateFromWallet(),unspentTxOut)
		# transactions.append(tra)
		# transactionAddr.append(tra.txOuts[0].address)
		# transactionCoins.append(tra.txOuts[0].amount)
		r=requests.post('http://127.0.0.1:16000/control/sendTransaction',json=request.data)
		data={"transactionNumber":1}
		return Response(data)

class transactionStatusView(APIView):
	def get(self,request):
		global myAddress
		pendingTx = requests.get('http://127.0.0.1:16000/control/getTransactionPool',params=request.data)
		print("pending",pendingTx.json())
		if(len(pendingTx.json())==0):
			transactionAddr=[]
			transactionCoins=[]
		else:
			txOut=[x['txOuts'] for x in pendingTx.json()]
			print(txOut)
			transactionAddr = [X['address'] for X in txOut[0] if X['address']==myAddress]
			transactionCoins = [X['amount'] for X in txOut[0] if X['address']==myAddress]
		completedTx = requests.get('http://127.0.0.1:16000/control/getAllBlocks',params=request.data)
		print("complete",completedTx.json())
		if(len(completedTx.json())==1):
			completedTxAddr= [addr['address'] for blocks in completedTx.json() for txs in blocks['data'] for addr in txs['txOuts'] if addr['address']==myAddress ] 
			completedTxAmt= [addr['amount'] for blocks in completedTx.json() for txs in blocks['data'] for addr in txs['txOuts'] if addr['address']==myAddress]
			completedTxSenderAddr= [addr['address'] for blocks in completedTx.json() for txs in blocks['data'] for addr in txs['txOuts'] if addr['address']==myAddress] 
		else:
			completedTxAddr=[txs['txOuts'][0]['address'] for blocks in completedTx.json() for txs in blocks['data'] if txs['txOuts'][1]['address']==myAddress]
			# completedTxAddr = [y['data'][0]['txOuts'][0]['address'] for y in completedTx.json() if y['data'][0]['txOuts'][0]['address']==myAddress]
			# completedTxAmt = [y['data'][0]['txOuts'][0]['amount'] for y in completedTx.json() if y['data'][0]['txOuts'][0]['address']==myAddress]	
			completedTxAmt=[txs['txOuts'][0]['amount'] for blocks in completedTx.json() for txs in blocks['data'] if txs['txOuts'][1]['address']==myAddress]
			completedTxSenderAddr=[txs['txOuts'][1]['address'] for blocks in completedTx.json() for txs in blocks['data'] if txs['txOuts'][1]['address']==myAddress]
		data={"transactionAddr":transactionAddr,"transactionCoins":transactionCoins,"completedTxAddr":completedTxAddr,"completedTxAmt":completedTxAmt,"completedTxSenderAddr":completedTxSenderAddr}
		print(data)
		return Response(data)

class publicAddressView(APIView):
	def get(self,request):
		global myAddress
		publicAddr = requests.get('http://127.0.0.1:16000/control/getWalletAddress',params=request.data)
		myAddress=publicAddr.json()['address']
		data={"publicKey":publicAddr.json()['address']}
		print(data)
		return Response(data)

class balanceView(APIView):
	def get(self,request):
		global myAddress
		#balance = w.getBalance(publicAddr,unspentTxOut)
		balance = requests.get('http://127.0.0.1:16000/control/getUnspentTxOuts',params=request.data)
		print(balance,balance.json())
		b = sum([t['amount'] for t in balance.json() if t['address']==myAddress])
		data={"balance":b}
		return Response(data)

class mineView(APIView):
	def put(self,request):
		requests.put('http://127.0.0.1:16000/control/mineBlock',params=request.data)

class logsView(APIView):
	def get(self,request):
		completedTx = requests.get('http://127.0.0.1:16000/control/getAllBlocks',params=request.data)
		logs=[]
		if(len(completedTx.json())==1):
			# receivedTxAddr= [addr['address'] for blocks in completedTx.json() for txs in blocks['data'] for addr in txs['txOuts'] if addr['address']==myAddress ] 
			txAmt= [addr['amount'] for blocks in completedTx.json() for txs in blocks['data'] for addr in txs['txOuts'] if addr['address']==myAddress]
			receivedTxSenderAddr= [addr['address'] for blocks in completedTx.json() for txs in blocks['data'] for addr in txs['txOuts'] if addr['address']==myAddress] 
			sentTxAddr=[]
			sentTxAmt=[]
			logs.append(["received",txAmt[0],receivedTxSenderAddr[0]])
		else:
			# txAmt=[]
			# receivedTxSenderAddr=[]
			# sentTxAddr=[]
			# sentTxAmt=[]
			for blocks in completedTx.json(): 
				for txs in blocks['data']: 
					if txs['txOuts'][0]['address']==myAddress:
						logs.append(["received",txs['txOuts'][0]['amount']],txs['txOuts'][1]['address'])
					elif txs['txOuts'][1]['address']==myAddress:
						logs.append(["sent",txs['txOuts'][0]['amount']],txs['txOuts'][0]['address'])
		data={"logs":logs}
		print(data)
		return Response(data)