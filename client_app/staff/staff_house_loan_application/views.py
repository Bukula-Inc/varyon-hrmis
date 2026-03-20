from django.shortcuts import render

# Create your views here.
def staff_house_loan_application(request):
    return render(request,  'staff_house_loan_application/dashboard.html')