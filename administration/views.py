from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *

# Create your views here.
def dashboard(request):
    return render(request, 'administration/dashboard.html')

def billing(request):
    return render(request, 'administration/billing.html')

def users(request):
    if not request.user.is_superuser: 
        raise Http404("Page not found") 

    # Get all users
    users_list = User.objects.all()
    # ---- ROLE FILTERING ----
    role = request.GET.get("role")   # role=staff / doctor / patient

    if role == "staff":
        users_list = users_list.exclude(profile__role="doctor").exclude(profile__role="patient")

    elif role == "doctor":
        users_list = users_list.filter(profile__role="doctor")

    elif role == "patient":
        users_list = users_list.filter(profile__role="patient")

    # Search
    username = request.GET.get('username')
    if username:
        users_list = users_list.filter(
            Q(username__icontains=username)
        )

    # Handle deletion
    if request.method == 'POST': 
        delete_id = request.POST.get('delete') 
        if delete_id: 
            user = get_object_or_404(User, id=delete_id) 
            user.delete() 
            messages.success(request, f'User {user.username} deleted successfully.') 
            return redirect('administration:users')

    # Pagination (always executed)
    paginator = Paginator(users_list, 5)  # 2 users per page
    page_number = request.GET.get('page') 
    users_page = paginator.get_page(page_number)

    context = { 
        "users": users_page,
        "paginator": paginator, 
        "page_number": page_number, 
        "role":role,
    } 
    return render(request, 'administration/users.html', context)

def new_user(request):
    # ---- ADMIN ONLY ACCESS ---- 
    if not request.user.is_superuser: # OR use role check 
        raise Http404("Page not found")
    
    if request.method == "POST": 
        username = request.POST.get("username") 
        phone_number = request.POST.get("phone_number") 
        address = request.POST.get("address") 
        gender = request.POST.get("gender") 
        role = request.POST.get("role")
        if username:
            user = User.objects.create_user(username=username)
            user.profile.phone_number = phone_number 
            user.profile.address = address 
            user.profile.gender = gender 
            user.profile.role = role .lower()
            user.save() 
            message = "User created successfully!" 
            return redirect('administration:users')
        else: message = "please provide complete information" 
        
    context = { 
        "message": message 
    } 
    return render(request, 'administration/users.html', context)
        
def edit_user(request, id):

    # ---- ADMIN ONLY ACCESS ----
    if not request.user.is_superuser:   # OR use role check
        raise Http404("Page not found")
    
    try:
       user = User.objects.get(id=id)
    except Exception as e:
        raise Http404(f"User does not exists with id: {id}")
    if request.method == "POST":
        username = request.POST.get('username')
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        role = request.POST.get("role")

        user.username = username
        user.profile.phone_number = phone_number
        user.profile.address = address
        user.profile.gender = gender
        user.profile.role = role .lower()
        user.save()
        return redirect('administration:users')
    context = {
        "user": user
    }
    return render(request, 'administration/users.html', context)

def tests(request):
    """ Test list with search + pagination + delete """
    search = request.GET.get("search", "")

    tests = MedicalTest.objects.all().order_by("-id")

    if search:
        tests = tests.filter(
            Q(name__icontains=search) |
            Q(code__icontains=search)
        )
    # Handle delete
    if request.method == "POST" and request.POST.get("delete"):
        test = get_object_or_404(MedicalTest, id=request.POST.get("delete"))
        test.delete()
        messages.success(request, "Test deleted successfully.")
        return redirect("administration:tests")
    # Pagination
    paginator = Paginator(tests, 20)
    page = request.GET.get("page")
    tests = paginator.get_page(page)
    context = {
        "tests":tests,
    }
    return render(request, "administration/tests.html", context)

def create_test(request):
    """ Create new medical test """
    if request.method == "POST":
        MedicalTest.objects.create(
            name=request.POST.get("name"),
            code=request.POST.get("code"),
            price=request.POST.get("price"),
            discount_type=request.POST.get("discount_type"),
            discount_value=request.POST.get("discount_value") or None,
            sample_type=request.POST.get("sample_type"),
            fasting_required=bool(request.POST.get("fasting_required")),
            processing_time_hours=request.POST.get("processing_time_hours") or 24, # default 24
            unit=request.POST.get("unit"),
            has_range=request.POST.get("has_range"),
            report_format=request.POST.get("report_format"),
            reference_range=request.POST.get("reference_range"),
            gender_specific=request.POST.get("gender_specific"),
            description=request.POST.get("description"),
            instructions=request.POST.get("instructions"),
            is_active=True,
        )
        messages.success(request, "New test added successfully.")
        return redirect("administration:tests")

def update_test(request, test_id):
    """ Update existing test """
    test = get_object_or_404(MedicalTest, id=test_id)

    if request.method == "POST":
        test.name = request.POST.get("name")
        test.code = request.POST.get("code")
        test.price = request.POST.get("price")
        test.discount_type = request.POST.get("discount_type") or None
        test.discount_value = request.POST.get("discount_value") or None
        test.sample_type = request.POST.get("sample_type")
        test.fasting_required = bool(request.POST.get("fasting_required"))
        test.processing_time_hours = request.POST.get("processing_time_hours")
        test.unit = request.POST.get("unit")
        test.has_range = request.POST.get("has_range")
        test.report_format = request.POST.get("report_format")
        test.reference_range = request.POST.get("reference_range")
        test.gender_specific = request.POST.get("gender_specific")
        test.description = request.POST.get("description")
        test.instructions = request.POST.get("instructions")
        test.save()
        messages.success(request, "Test updated successfully.")
        return redirect("administration:tests")