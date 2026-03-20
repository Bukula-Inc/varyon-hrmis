from django.shortcuts import render

# Create your views here.
def employee_seperation_dashboard(request):
    return render(request, 'employee_separation_dashboard/dashboard.html')