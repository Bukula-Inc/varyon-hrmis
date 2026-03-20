from django.shortcuts import render

# Create your views here.
def tution_advance_of_salary(request):
    return render(request, 'tution_advance_of_salary/dashboard.html')