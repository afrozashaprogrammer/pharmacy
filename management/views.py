from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.
@login_required(login_url="/accounts/login/")
def dashboard(request):
    return render(request, 'management/dashboard.html')

@login_required(login_url="/accounts/login/")
def counter_dashboard(request):
    profile = getattr(request.user, "profile", None)

    if not profile or profile.role != "counter":
        raise Http404("Page not found")

    return render(request, "management/counter/dashboard.html")