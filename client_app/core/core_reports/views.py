from django.shortcuts import render
# Create your views here.
def dashboard(request):      
    return render(request,'asset_maintenance_report/dashboard.html')