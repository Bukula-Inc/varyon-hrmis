from django.shortcuts import render

# Create your views here.
def skills_inventory(request):
    return render(request, 'skills_inventory_dashboard/dashboard.html')