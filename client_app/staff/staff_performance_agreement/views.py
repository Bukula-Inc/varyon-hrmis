from django.shortcuts import render

# Create your views here.
def staff_performance_agreement(request):
    return render(request, 'staff_performance_agreement/dashboard.html')