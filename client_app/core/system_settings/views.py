from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request, 'system_settings/dashboard.html')
