from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, "allowance_and_benefit/dashboard.html")