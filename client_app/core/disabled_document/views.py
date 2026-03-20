from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request, 'disabled_document/dashboard.html')
