from django.shortcuts import render

def index (request):
    return render (request, "staff_authority_to_council_car/index.html")