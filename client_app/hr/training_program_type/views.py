from django.shortcuts import render

# Create your views here.
def training_program_type(request):
    return render (request, 'training_program_type/dashboard.html')