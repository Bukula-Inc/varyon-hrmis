from django.shortcuts import render

# Create your views here.
def employee_selfare_report(request):
    return render(request, 'employee_welfare_report/dashboard.html')