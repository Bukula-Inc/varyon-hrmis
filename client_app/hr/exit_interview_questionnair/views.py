from django.shortcuts import render

# Create your views here.
def exit_interview_questionnair(request):
    return render(request, 'exit_interview_questionnair/dashboard.html')