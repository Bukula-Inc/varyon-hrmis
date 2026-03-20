from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, "staff_suggestion_box/dashboard.html")
