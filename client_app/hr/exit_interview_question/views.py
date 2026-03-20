from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, "exit_interview_question/dashboard.html")