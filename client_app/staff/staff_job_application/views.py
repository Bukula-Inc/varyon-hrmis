from django.shortcuts import render

def dashboard (request):
    return render (request, "staff_job_application/dashboard.html")
