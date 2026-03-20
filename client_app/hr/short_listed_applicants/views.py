from django.shortcuts import render

# Create your views here.
def short_listed_applicants(request):
    return render(request, 'short_listed_applicants/dashboard.html')