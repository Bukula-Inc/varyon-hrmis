from django.shortcuts import render

# Create your views here.
def bonus_weightage(request):
    return render(request, 'bonus_weightage/dashboard.html')