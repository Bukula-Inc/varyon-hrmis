from django.shortcuts import render

# Create your views here.
def bonus_threshold(request):
    return render(request, 'bonus_threshold/dashboard.html')