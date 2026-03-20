from django.shortcuts import render

# Create your views here.
def leave_commutation(request):
    return render(request, 'leave_commutation/dashboard.html')