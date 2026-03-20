from django.shortcuts import render

# Create your views here.
def appraisal_report (request):
    return render (request, "appraisal_report/dashboard.html")