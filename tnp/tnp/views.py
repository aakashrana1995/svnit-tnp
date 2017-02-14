from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
	if(request.user.is_authenticated):
		return HttpResponseRedirect('/consent/home')
	else:
		return HttpResponseRedirect('/consent/login')
