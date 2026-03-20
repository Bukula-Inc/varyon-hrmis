from django.shortcuts import render

# Create your views here.
def short_listed_applicants_report(request):
    return render(request, "short_listed_applicants_report/dashboard.html")