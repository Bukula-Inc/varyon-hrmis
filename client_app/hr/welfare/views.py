from django.shortcuts import render

# Create your views here.
def welfare(request):
    return render(request, 'welfare/dashboard.html')