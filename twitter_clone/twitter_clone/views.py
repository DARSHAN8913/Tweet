from django.shortcuts import render

def home(request):
    return render(request, 'homee.html')  # Ensure 'home.html' exists in templates

def register_page(request):
    return render(request, 'register.html')