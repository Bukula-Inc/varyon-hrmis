from django.shortcuts import render

def dashboard(request):
    return render(request, 'amendments_report/dashboard.html')