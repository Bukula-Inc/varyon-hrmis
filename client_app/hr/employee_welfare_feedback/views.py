from django.shortcuts import render

# Create your views here.
def employee_welfare_feedback(request):
    return render(request, 'employee_welfare_feedback/dashboard.html')