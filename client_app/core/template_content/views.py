from django.shortcuts import render

# Create your views here.
def template_content(request):
    return render(request, 'template_content/dashboard.html')