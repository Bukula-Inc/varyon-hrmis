from django.shortcuts import render

# Create your views here.
def staff_work_plan_report(request):
    return render(request, 'staff_work_plan_report/dashboard.html')