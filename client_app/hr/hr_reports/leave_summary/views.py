from django.shortcuts import render

# Create your views here.
def leave_summary(request):
    return render(request, 'leave_summary/dashboard.html')