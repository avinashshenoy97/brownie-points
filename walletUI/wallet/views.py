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
def wallet(request):
	w.initWallet()
	unspentTxOut.append(t.getCoinbaseTransaction(publicAddr, 0))
	return render(request, "index.html",context)

class sendCoinsView(APIView):
	def put(self,request):
		print("put",request.data)
		# unspentTxOut=w.createTransaction(request.data['address'],request.data['coinCount'],publicAddr,unspentTxOut)
		data={"Coins":"Sent"}
		return Response(data)

class transactionStatusView(APIView):
	def get(self,request):
		data={"transaction":"status"}
		return Response(data)

class publicAddressView(APIView):
	def get(self,request):
		data={"publicKey":publicAddr}
		print(data)
		return Response(data)

class balanceView(APIView):
	def get(self,request):
		balance = getBalance(publicAddr,unspentTxOut)
		data={"balance":balance}
		return Response(data)
