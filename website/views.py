from controllers.web import Web_Controller
from django.shortcuts import render

def unauthorized (request):
    return render (request, "authentication/unauthorized.html")

def dynamic_page_render(request, page="home"):
    wc = Web_Controller(request, page)
    return wc.render_page()

def careers (request):
    return render (request, "website/main/careers.html")

def features (request):
    return render (request, "website/main/features.html")

def about (request):
    return render (request, "website/main/about.html")

def job_offer (request):
    return render (request, "website/main/job_offer.html")

def appointment_letter (request):
    return render (request, "website/main/appointment_letter.html")

def medical_police_clearance (request):
    return render (request, "website/main/medical_clearance.html")
def upload_medical_clearance (request):
    return render (request, "website/main/upload_medical_clearance.html")