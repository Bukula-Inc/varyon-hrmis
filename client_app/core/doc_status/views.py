from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'doc_status/dashboard.html')