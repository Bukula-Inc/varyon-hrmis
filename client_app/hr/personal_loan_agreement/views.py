from django.shortcuts import render

# Create your views here.
def personal_loan_agreement(request):
    return render(request, "personal_loan_agreement/dashboard.html")