from django.shortcuts import render

# Create your views here.
def employee_advance_summary (request):
    return render (request, "employee_advance_summary/dashboard.html")