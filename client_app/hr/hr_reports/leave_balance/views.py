from django.shortcuts import render

# Create your views here.
def leave_balance (request):
    return render (request, "leave_balance/dashboard.html")