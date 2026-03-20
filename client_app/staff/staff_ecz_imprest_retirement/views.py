from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'staff_ecz_imprest_retirement/dashboard.html')