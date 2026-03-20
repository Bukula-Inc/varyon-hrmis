from django.shortcuts import render

# Create your views here.
def skill_levy(request):
    return render(request, 'skill_levy/dashboard.html')