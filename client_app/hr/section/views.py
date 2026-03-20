from django.shortcuts import render

# Create your views here.
def bonus(request):
    return render(request, 'section/dashboard.html')