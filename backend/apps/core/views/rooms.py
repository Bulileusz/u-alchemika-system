from django.shortcuts import render

from ..models import Room

def index(request):
    return render(request, 'index.html')

