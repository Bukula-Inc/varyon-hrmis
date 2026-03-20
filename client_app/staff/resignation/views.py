from django.shortcuts import render

# Create your views here.
def resgnation(request):
    return render(request, "resignation/dashboard.html")