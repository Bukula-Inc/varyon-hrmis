from django.shortcuts import render

def dashboard (request):
    return render (request, "staff_employee_feedback/dashboard.html")
