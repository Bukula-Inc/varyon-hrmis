from django.shortcuts import render

def dashboard (request):
    return render (request, "staff_employee_files/dashboard.html")
