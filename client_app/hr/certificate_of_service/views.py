from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'certificate_of_service/dashboard.html')