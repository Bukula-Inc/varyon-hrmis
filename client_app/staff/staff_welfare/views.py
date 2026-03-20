from django.shortcuts import render

# Create your views here.
def staff_welfare(request):
    return render(request, 'staff_welfare/dashboard.html')