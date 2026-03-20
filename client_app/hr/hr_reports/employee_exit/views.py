from django.shortcuts import render

# Create your views here.
def employee_exit (request):
    return render (request, "employee_exit/dashboard.html")