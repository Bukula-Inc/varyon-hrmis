from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, "cash_repayment/dashboard.html")