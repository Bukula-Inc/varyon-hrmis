from django.shortcuts import render

# Create your views here.
def staff_leave_commutation(request):
    return render(request, 'staff_leave_commutation/dashboard.html')