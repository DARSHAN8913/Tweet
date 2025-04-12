from django.shortcuts import render
# from django.contrib.auth import login

def home(request):
    return render(request, 'hm.html')  # Ensure 'home.html' exists in templates

def register_page(request):
    return render(request, 'registration/register.html')

def login_page(request):
    return render(request, 'registration/login.html')  # Adjust path if needed


def profile_view(request, username):
    # You can later query user-specific data using this username
    context = {'username': username}
    return render(request, 'profile.html', context)