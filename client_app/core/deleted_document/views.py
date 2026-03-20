from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request, 'deleted_document/dashboard.html')
