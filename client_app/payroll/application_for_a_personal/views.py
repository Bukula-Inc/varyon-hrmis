from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, "application_for_a_personal/dashboard.html")