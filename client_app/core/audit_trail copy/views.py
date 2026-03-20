from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request, 'audit_trail/dashboard.html')
