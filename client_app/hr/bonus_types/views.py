from django.shortcuts import render

# Create your views here.
def bonus_type(request):
    return render(request, 'bonus_types/dashboard.html')