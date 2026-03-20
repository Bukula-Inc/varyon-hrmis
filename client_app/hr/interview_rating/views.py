from django.shortcuts import render

# Create your views here.
def interview_rating (request):
    return render(request, 'interview_rating/dashboard.html')