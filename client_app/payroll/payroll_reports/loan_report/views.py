from django.shortcuts import render

# Create your views here.
def appraisal_report (request):
    return render (request, "loan_report/dashboard.html")