from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
context={}
def explorer(request):
	return render(request, "index.html",context)


class poolDataView(APIView):
	def get(self,request):
		pendingTx = requests.get('http://127.0.0.1:16000/control/getTransactionPool',params=request.data)
		if(len(pendingTx.json())==0):
			transactionAddr=[]
			transactionCoins=[]
		else:
			txOut=[x['txOuts'] for x in pendingTx.json()]
			transactionAddr = [X['address'] for X in txOut[0]]
			transactionCoins = [X['amount'] for X in txOut[0]]
		data={"transactionAddr":transactionAddr,"transactionCoins":transactionCoins}
		print(data)
		return Response(data)