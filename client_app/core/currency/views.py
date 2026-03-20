from django.shortcuts import render
# Create your views here.


def dashboard(request):
    return render(request, 'currency/dashboard.html')
