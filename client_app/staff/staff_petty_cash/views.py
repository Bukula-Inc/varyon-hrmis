from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'staff_petty_cash/dashboard.html')