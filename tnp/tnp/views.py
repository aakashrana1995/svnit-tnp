from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
	if(request.user.is_authenticated):
		return HttpResponseRedirect('/consent/home')
	else:
		return render(request, 'index.html', {})

def about(request):
	return render(request, 'about.html', {})
