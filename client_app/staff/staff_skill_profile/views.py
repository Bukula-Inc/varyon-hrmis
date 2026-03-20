from django.shortcuts import render

# Create your views here.
def staff_skill_profile(request):
    return render(request, 'staff_skill_profile/dashboard.html')