from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
# Create your views here.
context={}
myAddress=''

def explorer(request):
	return render(request, "index.html",context)

class poolDataView(APIView):
	def get(self,request):
		global myAddress
		publicAddr = requests.get('http://127.0.0.1:16000/control/getWalletAddress',params=request.data)
		myAddress=publicAddr.json()['address']
		
		pendingTx = requests.get('http://127.0.0.1:16000/control/getTransactionPool',params=request.data)
		if(len(pendingTx.json())==0):
			transactionAddr=[]
			transactionCoins=[]
			transactionAddrSender=[]
		else:
			transactionAddr = [x['txOuts'][0]['address'] for x in pendingTx.json() if x['txOuts'][1]['address']==myAddress]
			transactionCoins = [x['txOuts'][0]['amount'] for x in pendingTx.json() if x['txOuts'][1]['address']==myAddress]
			transactionAddrSender = [x['txOuts'][1]['address'] for x in pendingTx.json() if x['txOuts'][1]['address']==myAddress]
		data={"transactionAddr":transactionAddr,"transactionCoins":transactionCoins,"transactionAddrSender":transactionAddrSender}
		print(data)
		return Response(data)