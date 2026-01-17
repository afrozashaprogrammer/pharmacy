from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from administration.models import * 
from accounts.models import * 
from administration.forms import PatientForm
from .models import *


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

    doctors = User.objects.filter(profile__role='doctor')
    # Patients for dropdown
    patients = User.objects.filter(profile__role='patient')
    # Active medical tests
    medical_tests = MedicalTest.objects.filter(is_active=True)
    context = {
        "staff": doctors,       # এখানে staff মানে doctor
        "patients": patients,
        "medical_tests": medical_tests,
    }

    return render(request, "management/counter/patient_test_form.html", context)

@login_required
def patient_search(request):
    q = request.GET.get("patient_search", "")
    patients = User.objects.filter(
        profile__role="patient"
    ).filter(
        Q(first_name__icontains=q) |
        Q(last_name__icontains=q) |
        Q(username__icontains=q)
    )[:10]

    return render(
        request,
        "management/counter/htmx/patient_results.html",
        {"patients": patients}
    )
@login_required
def patient_select(request, pk):
    patient = User.objects.get(pk=pk)
    return render(
        request,
        "management/counter/htmx/patient_selected.html",
        {"patient": patient}
    )

@login_required
def patient_create_form(request):
    form = PatientForm()
    return render(
        request,
        "management/counter/htmx/patient_create_form.html",
        {"form": form}
    )
@login_required
def patient_create(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.save()
            # ensure profile role = patient
            profile = getattr(patient, 'profile', None)
            if not profile:
                profile = Profile.objects.create(user=patient, role='patient')
            else:
                profile.role = 'patient'
                profile.save()
            # return patient_selected partial
            return render(
                request,
                "management/counter/htmx/patient_selected.html",
                {"patient": patient}
            )
        else:
            # return form with errors
            return render(
                request,
                "management/counter/htmx/patient_create_form.html",
                {"form": form}
            )
    return HttpResponse(status=400)


