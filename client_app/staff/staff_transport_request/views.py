from django.shortcuts import render

# Create your views here.
def transport_request(request):
    return render(request, 'staff_transport_request/dashboard.html')