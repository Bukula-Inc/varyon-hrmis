from django.shortcuts import render

# Create your views here.
def dashboard (request):
    return render (request, "payroll_loans_dashboard/dashboard.html")