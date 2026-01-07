from django.shortcuts import redirect

def home(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.is_superuser:
        return redirect('administration:dashboard')

    return redirect('management:dashboard')