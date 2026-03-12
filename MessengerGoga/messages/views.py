from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
  
def goga(request):
    return HttpResponse("МЕССЕНДЖЕР ГЕОРГИЙ")

def secret(request):
    return HttpResponse("Как ты сюда попал???")

def reg(request):
    return render(request, "reg.html")
