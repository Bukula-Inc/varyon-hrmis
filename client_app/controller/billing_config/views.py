from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'billing_config/dashboard.html')