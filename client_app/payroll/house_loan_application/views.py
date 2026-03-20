from django.shortcuts import render

# Create your views here.
def house_loan_application(request):
    return render(request, 'house_loan_application/dashboard.html')