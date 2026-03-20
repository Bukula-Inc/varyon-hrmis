from django.shortcuts import render

# Create your views here.
def training_ffedback_report(request):
    return render(request, 'training_feedback_report/dashboard.html')