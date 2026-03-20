from django.shortcuts import render

def dashboard (request):
    return render (request, "overtime_claim/dashboard.html")