# chat/views.py
from django.shortcuts import render

def message(request):
    return render(request, 'nano_poker/stats.html')

def index(request):
    return render(request, 'nano_poker/index.html')