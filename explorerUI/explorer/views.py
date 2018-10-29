from django.shortcuts import render

# Create your views here.
context={}
def explorer(request):
	return render(request, "index.html",context)