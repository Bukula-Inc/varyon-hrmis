from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.


def dashboard(request):
    
    return render(request, 'employee/dashboard.html')


def employee_list(request):
    
    return render(request, 'employee/employee.html')


def employee_checkin_create(request):
    
    return render(request, 'employee/employee_checkin_create.html')


def attendance(request):
    
    return render(request, 'employee/attendance.html')


def checkin(request):
    
    return render(request, 'employee/checkin.html')


def attendance_create(request):
    
    return render(request, 'employee/attendance_create.html')


def monthly_attendance_sheet(request):
    
    return render(request, 'employee/monthly_attendance_sheet.html')


def employee_information(request):
    
    return render(request, 'employee/employee_information.html')


def salary_advance_create(request):
    
    return render(request, 'employee/create_advance.html')


def salary_advance_list(request):
    
    return render(request, 'employee/advance.html')


def promotion(request):
    
    return render(request, 'employee/promotion.html')


def employee_promotion_create(request):
    
    return render(request, 'employee/employee_promotion.html')


def branch_create(request):
    
    return render(request, 'branch/branch_create.html')


def branch(request):
    
    return render(request, 'branch/branch.html')


def employee_birthday(request):
    
    return render(request, 'employee/employee_birthday.html')


def employee_advance_summary(request):
    
    return render(request, 'employee/advance_summary.html')


def employee_exit(request):
    
    return render(request, 'employee/employee_exit.html')


def employee_contacts(request):
    
    return render(request, 'employee/employee_contacts_&others.html')
