from django.shortcuts import render

# Create your views here.
def bonus_setting(request):
    return render(request, 'bonus_settings/dashboard.html')