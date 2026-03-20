from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
def dashboard(request):
    return render(request, 'hr/dashboard.html')

def leave(request):
    return render(request, 'hr/leave_create.html')

