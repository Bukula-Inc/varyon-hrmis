from django.shortcuts import render

# Create your views here.
def training_program_application(request):
    return render(request, 'training_program_application/dashboard.html')