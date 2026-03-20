from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request, 'form_customization/dashboard.html')
