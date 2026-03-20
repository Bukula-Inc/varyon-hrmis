from django.shortcuts import render

# Create your views here.
def training_program_feedback(request):
    return render(request, 'training_program_feedback/dashboard.html')