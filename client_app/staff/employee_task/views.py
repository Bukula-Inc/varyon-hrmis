from django.shortcuts import render

# Create your views here.
def employee_tasks(request):
    return render(request, 'employee_task/dashboard.html')