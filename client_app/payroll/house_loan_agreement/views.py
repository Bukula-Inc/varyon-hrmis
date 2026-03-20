from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'house_loan_agreement/dashboard.html')