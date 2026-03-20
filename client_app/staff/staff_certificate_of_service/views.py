from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'staff_certificate_of_service/dashboard.html')