from django.shortcuts import render

# Create your views here.
def staff_welfare(request):
    return render(request, 'staff_clearance_form/dashboard.html')