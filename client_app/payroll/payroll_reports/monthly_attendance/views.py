from django.shortcuts import render

# Create your views here.
def monthly_attendance(request):
    return render(request, 'monthly_attendance/dashboard.html')