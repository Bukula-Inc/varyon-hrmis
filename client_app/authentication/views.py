from django.shortcuts import render

def login(request):
    return render(request, 'authentication/login.html')

def reset_password (request): 
    return render (request, 'authentication/password_reset.html')

def logout (request): 
    return render (request, 'authentication/logout.html')