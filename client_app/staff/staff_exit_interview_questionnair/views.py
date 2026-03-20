from django.shortcuts import render

# Create your views here.
def staff_exit_interview_questionnair(request):
    return render(request, 'staff_exit_interview_questionnair/dashboard.html')