from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.models import User
from administration.models import MedicalTest  # import from admin app


# Create your views here.
@login_required(login_url="/accounts/login/")
def dashboard(request):
    return render(request, 'management/dashboard.html')

@login_required(login_url="/accounts/login/")
def counter_dashboard(request):
    profile = getattr(request.user, "profile", None)
    if not profile or profile.role != "counter":
        raise Http404("Page not found")

    return render(request, "management/counter/counter_dashboard.html")

@login_required(login_url="/accounts/login/")
def patient_test(request):
    # Patients for dropdown
    patients = User.objects.filter(profile__role='patient')
    # Staff for referred_by dropdown
    staff = User.objects.filter(profile__role='doctor')
    # Active medical tests
    medical_tests = MedicalTest.objects.filter(is_active=True)
    context = {
        "patients": patients,
        "staff": staff,
        "medical_tests": medical_tests,
    }

    return render(request, "management/counter/patient_test_form.html", context)
