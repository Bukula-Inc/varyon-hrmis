from django.shortcuts import render

# Create your views here.
def employee_resignation(request):
    return render(request, 'employee_resignation/dashboard.html')