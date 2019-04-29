from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def toolhome(request):
    return HttpResponse('Tool Home')