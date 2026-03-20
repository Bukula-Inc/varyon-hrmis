from django.shortcuts import render

def dashboard(request):
    return render(request, 'transfer_file/dashboard.html')