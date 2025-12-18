from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as signin
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request, 'accounts/home.html')
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Username and password are required")
            return render(request, 'accounts/login.html')

        user = authenticate(request, username=username, password=password)
        if user:
            signin(request, user)  # Log in the user

            # Redirect based on superuser or normal user
            if user.is_superuser:
                return redirect('administration:dashboard')
            else:
                return redirect('management:dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'accounts/login.html')