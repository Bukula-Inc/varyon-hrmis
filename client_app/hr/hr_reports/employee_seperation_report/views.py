from django.shortcuts import render

# Create your views here.
def employee_seperation_report(request):
    return render(request, 'employee_seperation_report/dashboard.html')