from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request, 'advanced_access_control/dashboard.html')
