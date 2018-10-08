from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
main_dir = os.path.dirname(parentdir)
sys.path.insert(0,main_dir)
print(sys.path)

from browniePoints import wallet as w
from browniePoints import transaction as t
# Create your views here.
context={}
publicAddr=w.getPublicFromWallet()
unspentTxOut=[]
transactions=[]
transactionAddr=[]
transactionCoins=[]

w.initWallet()
trans,usp = t.getCoinbaseTransaction(publicAddr,0)
unspentTxOut.append(usp)
transactions.append(trans)
def wallet(request):
	return render(request, "index.html",context)

class sendCoinsView(APIView):
	def put(self,request):
		global unspentTxOut
		print("put",request.data)
		tra = w.createTransaction(request.data['address'],request.data['coinCount'],w.getPrivateFromWallet(),unspentTxOut)
		transactions.append(tra)
		transactionAddr.append(tra.txOuts[0].address)
		transactionCoins.append(tra.txOuts[0].amount)
		data={"transactionNumber":len(transactionAddr)}
		return Response(data)

class transactionStatusView(APIView):
	def get(self,request):
		data={"transactionAddr":transactionAddr,"transactionCoins":transactionCoins}
		print(data)
		return Response(data)

class publicAddressView(APIView):
	def get(self,request):
		data={"publicKey":publicAddr}
		print(data)
		return Response(data)

class balanceView(APIView):
	def get(self,request):
		balance = w.getBalance(publicAddr,unspentTxOut)
		data={"balance":balance}
		return Response(data)
