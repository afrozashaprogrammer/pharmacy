from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as signin

# Create your views here.
def home (request):
    return render (request, 'accounts/home.html')
def login(request):
    message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                signin(request, user)
                return redirect('administration:dashboard')
            else:
                message = "Invalid username or password"
        else:
            message = "Username and password is required"

    context = {
        "message": message
    }
    return render(request, 'accounts/login.html', context)
