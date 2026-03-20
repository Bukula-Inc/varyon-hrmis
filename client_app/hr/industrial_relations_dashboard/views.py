from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def dashboard (request):
    return render (request, "industrial_relations_dashboard/dashboard.html")