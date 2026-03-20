from django.shortcuts import render

# Create your views here.
def verbal_warning(request):
    return render(request, 'verbal_warning/dashboard.html')