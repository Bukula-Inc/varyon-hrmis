from django.shortcuts import render

# Create your views here.
def employee_skill_distribution_dashboard(request):
        return render(request, 'employee_skill_distribution_dashboard/dashboard.html')