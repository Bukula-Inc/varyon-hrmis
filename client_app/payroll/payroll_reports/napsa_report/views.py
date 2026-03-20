from django.shortcuts import render

# Create your views here.
def napsa_report(request):
    return render(request, 'napsa_report/dashboard.html')