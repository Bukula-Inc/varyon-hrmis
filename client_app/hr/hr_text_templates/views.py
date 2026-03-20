from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.


def dashboard(request):
    
    return render(request, 'hr_text_templates/dashboard.html')