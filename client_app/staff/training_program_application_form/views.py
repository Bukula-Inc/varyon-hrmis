from django.shortcuts import render

# Create your views here.
def training_program_application_form(request):
    return render(request, 'training_program_application_form/dashboard.html')