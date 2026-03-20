from django.shortcuts import render

# Create your views here.
def dashboard (request):
    return render (request, "interview_panel/dashboard.html")