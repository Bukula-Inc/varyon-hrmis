from django.shortcuts import render

# Create your views here.
def bonus_planing(request):
    return render(request, 'bonus_planing/dashboard.html')