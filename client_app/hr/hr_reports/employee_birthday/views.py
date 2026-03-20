from django.shortcuts import render

# Create your views here.
def employee_birthday (request):
    return render (request, "employee_birthday/dashboard.html")