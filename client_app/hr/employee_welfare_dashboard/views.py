from django.shortcuts import render

# Create your views here.
def employee_welfare_dashboard(request):
    return render(request, 'employee_welfare_dashboard/dashboard.html')