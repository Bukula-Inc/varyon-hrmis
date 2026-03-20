from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, "petty_cash/dashboard.html")