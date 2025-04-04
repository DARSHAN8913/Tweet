from django.shortcuts import render
from django.contrib.auth import login

def home(request):
    return render(request, 'homee.html')  # Ensure 'home.html' exists in templates

def register_page(request):
    return render(request, 'registration/register.html')