from django.shortcuts import render

# Create your views here.
def priority(request):
    return render(request, 'priority/dashboard.html')