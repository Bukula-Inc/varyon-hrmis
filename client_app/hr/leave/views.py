from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.



def leave_create(request):
    
    return render(request, 'leave/leave_create.html')

def leave_list(request):
    
    return render(request, 'leave/leave.html')

def employee_leave_balance(request):
    
    return render(request, 'leave/employee_leave_balance.html')

def leave_allocation(request):
    
    return render(request, 'leave/leave_allocation.html')

def leave_allocation_create(request):
    
    return render(request, 'leave/leave_allocation_create.html')

def leave_type(request):
    
    return render(request, 'leave/leave_type.html')

def leave_create(request):
    
    return render(request, 'leave/leave_type_create.html')