from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'staff_purchase_requisition/dashboard.html')