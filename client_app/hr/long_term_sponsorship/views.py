from django.shortcuts import render

# Create your views here.
def dashboard (request):
    return render (request, 'long_term_sponsorship/dashboard.html')