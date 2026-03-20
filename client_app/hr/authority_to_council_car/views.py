from django.shortcuts import render

def index (request):
    return render (request, "authority_to_council_car/index.html")