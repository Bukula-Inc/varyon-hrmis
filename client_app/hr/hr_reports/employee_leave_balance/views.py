from django.shortcuts import render

# Create your views here.
def employee_leave_balance (request):
    return render (request, "employee_leave_balance/dashboard.html")