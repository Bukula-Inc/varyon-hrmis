from django.shortcuts import render

# Create your views here.
def paye_report(request):
    return render(request, 'paye_report/dashboard.html')