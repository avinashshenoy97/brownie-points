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

context={}
myAddress=''
def wallet(request):
	return render(request, "index.html",context)

class sendCoinsView(APIView):
	def put(self,request):
		print("put",request.data)
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
			transactionAddrSender=[]
		else:
			transactionAddr = [x['txOuts'][0]['address'] for x in pendingTx.json() if x['txOuts'][1]['address']==myAddress]
			transactionCoins = [x['txOuts'][0]['amount'] for x in pendingTx.json() if x['txOuts'][1]['address']==myAddress]
			transactionAddrSender = [x['txOuts'][1]['address'] for x in pendingTx.json() if x['txOuts'][1]['address']==myAddress]
		completedTx = requests.get('http://127.0.0.1:16000/control/getAllBlocks',params=request.data)
		print("complete",completedTx.json())
		completedTxAddr=[]
		completedTxAmt=[]
		completedTxSenderAddr=[]
		for blocks in completedTx.json():
			for txs in blocks['data']:
				if(len(txs['txOuts'])==1):
					if txs['txOuts'][0]['address']==myAddress:
						completedTxAddr.append(txs['txOuts'][0]['address'])
						completedTxAmt.append(txs['txOuts'][0]['amount'])
						completedTxSenderAddr.append(txs['txOuts'][0]['address'])
				else:
					if txs['txOuts'][1]['address']==myAddress:
						completedTxAddr.append(txs['txOuts'][0]['address'])
						completedTxAmt.append(txs['txOuts'][0]['amount'])
						completedTxSenderAddr.append(txs['txOuts'][1]['address'])
		data={"transactionAddr":transactionAddr,"transactionCoins":transactionCoins,"transactionAddrSender":transactionAddrSender,"completedTxAddr":completedTxAddr,"completedTxAmt":completedTxAmt,"completedTxSenderAddr":completedTxSenderAddr}
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
		for blocks in completedTx.json(): 
			for txs in blocks['data']:
				if(len(txs['txOuts'])==1):
					if(txs['txOuts'][0]['address']==myAddress):
						logs.append(["received",txs['txOuts'][0]['amount'],txs['txOuts'][0]['address']])
				elif txs['txOuts'][0]['address']==myAddress:
					logs.append(["received",txs['txOuts'][0]['amount'],txs['txOuts'][1]['address']])
				elif txs['txOuts'][1]['address']==myAddress:
					logs.append(["sent",txs['txOuts'][0]['amount'],txs['txOuts'][0]['address']])
		data={"logs":logs}
		print(data)
		return Response(data)