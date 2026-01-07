from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as signin
from django.contrib.auth import logout as django_logout
from django.contrib import messages
# Create your views here.

def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('administration:dashboard')
        else:
            return redirect('management:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Username and password are required")
            return render(request, 'accounts/login.html')

        user = authenticate(request, username=username, password=password)
        if user:
            signin(request, user)

            if user.is_superuser:
                return redirect('administration:dashboard')
            else:
                return redirect('management:dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'accounts/login.html')

def logout(request):
    """Log the user out and redirect to login page."""
    django_logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('accounts:login')  # replace with your login URL name