from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'private_insurance_report/dashboard.html')