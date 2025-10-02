from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Home Page") 