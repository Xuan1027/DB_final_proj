from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
  
  return HttpResponse("Hello, Django. Nice 2 meet you.")