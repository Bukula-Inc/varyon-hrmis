from django.shortcuts import render

# Create your views here.
def hr_budget(request):
    return render(request, 'hr_budget/dashboard.html')