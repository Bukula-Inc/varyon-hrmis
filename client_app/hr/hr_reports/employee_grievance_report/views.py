from django.shortcuts import render

# Create your views here.
def employee_grievance_report(request):
    return render (request, "employee_grievance_report/dashboard.html")