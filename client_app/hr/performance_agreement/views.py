from django.shortcuts import render

# Create your views here.
def dashboard (request):
    return render (request, 'performance_agreement/dashboard.html')