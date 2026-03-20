from django.shortcuts import render

def index (request):
    return render (request, "staff_sitting_allowance_claim/index.html")