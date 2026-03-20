from django.shortcuts import render

# Create your views here.
def self_appraisal_report (request):
    return render (request, "self_appraisal_report/dashboard.html")