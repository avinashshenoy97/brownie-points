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
		pendingTx = requests.get('http://127.0.0.1:16000/control/getTransactionPool',params=request.data)
		print("pending",pendingTx.json())
		if(len(pendingTx.json())==0):
			transactionAddr=[]
			transactionCoins=[]
		else:
			txOut=[x['txOuts'] for x in pendingTx.json()]
			print(txOut)
			transactionAddr = [X['address'] for X in txOut[0]]
			transactionCoins = [X['amount'] for X in txOut[0]]
		completedTx = requests.get('http://127.0.0.1:16000/control/getAllBlocks',params=request.data)
		print("complete",completedTx.json())
		if(len(completedTx.json())==0):
			completedTxAddr=[]
			completedTxAmt=[]
		else:
			completedTxAddr = [y['data'][0]['txOuts'][0]['address'] for y in completedTx.json()]
			completedTxAmt = [y['data'][0]['txOuts'][0]['amount'] for y in completedTx.json()]	
		data={"transactionAddr":transactionAddr,"transactionCoins":transactionCoins,"completedTxAddr":completedTxAddr,"completedTxAmt":completedTxAmt}
		print(data)
		return Response(data)

class publicAddressView(APIView):
	def get(self,request):
		publicAddr = requests.get('http://127.0.0.1:16000/control/getWalletAddress',params=request.data)
		data={"publicKey":publicAddr.json()['address']}
		print(data)
		return Response(data)

class balanceView(APIView):
	def get(self,request):
		#balance = w.getBalance(publicAddr,unspentTxOut)
		balance = requests.get('http://127.0.0.1:16000/control/getUnspentTxOuts',params=request.data)
		print(balance,balance.json())
		b = sum([t['amount'] for t in balance.json()])
		data={"balance":b}
		return Response(data)

class mineView(APIView):
	def put(self,request):
		requests.put('http://127.0.0.1:16000/control/mineBlock',params=request.data)

class logsView(APIView):
	def get(self,request):
		loggedTx=requests.get('http://127.0.0.1:16000/control/getAllBlocks',params=request.data)
		logs=[y['data'][0]['txOuts'][0]['amount'] for y in loggedTx.json()]
		data={"logs":logs}
		print(data)
		return Response(data)