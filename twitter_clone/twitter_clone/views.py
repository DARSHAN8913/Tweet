from django.shortcuts import render

def home(request):
    return render(request, 'homee.html')  # Ensure 'home.html' exists in templates
