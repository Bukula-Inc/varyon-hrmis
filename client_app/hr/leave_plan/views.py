from django.shortcuts import render

def dashboard(request):
    
    return render(request, 'leave_plan/dashboard.html')