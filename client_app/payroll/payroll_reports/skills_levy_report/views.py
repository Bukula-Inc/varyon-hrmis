from django.shortcuts import render

# Create your views here.
def skills_levy_report(request):
    return render(request, 'skills_levy_report/dashboard.html')