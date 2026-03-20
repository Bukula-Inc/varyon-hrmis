from django.shortcuts import render

# Create your views here.
def welfare_type(request):
    return render(request, 'welfare_type/dashboard.html')