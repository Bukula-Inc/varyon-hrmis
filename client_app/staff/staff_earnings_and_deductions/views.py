from django.shortcuts import render

def dashboard (request):
    return render (request, "staff_earnings_and_deductions/dashboard.html")
