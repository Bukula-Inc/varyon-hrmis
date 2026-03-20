from django.shortcuts import render

# Create your views here.
def budget_line(request):
    return render(request, 'budget_line/dashboard.html')