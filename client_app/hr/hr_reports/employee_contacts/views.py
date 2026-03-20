from django.shortcuts import render

# Create your views here.
def employee_contacts (request):
    return render (request, "employee_contacts/dashboard.html")