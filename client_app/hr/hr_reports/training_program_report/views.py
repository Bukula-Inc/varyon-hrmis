from django.shortcuts import render

# Create your views here.
def training_program_report(request):
    return render(request, 'training_program_report/dashboard.html')