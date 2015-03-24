from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("yo sup")

def about(request):
	return HttpResponse("about me")
