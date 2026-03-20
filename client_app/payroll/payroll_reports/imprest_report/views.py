from django.shortcuts import render

# Create your views here.
def appraisal_report (request):
    return render (request, "imprest_report/dashboard.html")