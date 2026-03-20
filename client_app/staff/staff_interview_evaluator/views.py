from django.shortcuts import render

# Create your views here.
def staff_interview_evaluator(request):
    return render(request, 'staff_interview_evaluator/dashboard.html')