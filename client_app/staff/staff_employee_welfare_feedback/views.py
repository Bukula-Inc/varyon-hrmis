from django.shortcuts import render

# Create your views here.
def staff_employee_welfare_feedback(request):
    return render(request, 'staff_employee_welfare_feedback/dashboard.html')