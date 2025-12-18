from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *

# Create your views here.
@login_required(login_url="/accounts/login/")
def dashboard(request):
    return render(request, 'administration/dashboard.html')

def billing(request):
    return render(request, 'administration/billing.html')

def users(request):
    if not request.user.is_superuser:
        raise Http404("Page not found")

    role = request.GET.get("role", "staff")  # default staff
    search = request.GET.get("username", "")
    
    users_list = User.objects.all()
    
    # ---- ROLE FILTERING ----
    if role == "staff":
        users_list = users_list.exclude(profile__role__in=["doctor", "patient"])
    elif role in ["doctor", "patient"]:
        users_list = users_list.filter(profile__role=role)
    
    # ---- SEARCH ----
    if search:
        users_list = users_list.filter(
            Q(username__icontains=search) |
            Q(profile__phone_number__icontains=search)
        )
    
    # ---- DELETE ----
    if request.method == "POST" and request.POST.get("delete"):
        delete_id = request.POST.get("delete")
        user = get_object_or_404(User, id=delete_id)
        user.delete()
        messages.success(request, f"User {user.username} deleted successfully.")
        return redirect(f"/administration/users/?role={role}")

    # ---- PAGINATION ----
    paginator = Paginator(users_list, 3)  # 3 users per page
    page_number = request.GET.get("page")
    users_page = paginator.get_page(page_number)
    
    context = {
        "users": users_page,
        "paginator": paginator,
        "page_number": page_number,
        "role": role,
        "search": search,
    }

    # HTMX handling
    if request.headers.get("HX-Request") == "true":
        if request.GET.get("type") == "search":
            return render(request, "administration/htmx/user_search_result.html", context)
        elif request.GET.get("type") == "pagination":
            return render(request, "administration/htmx/user_table.html", context)
    
    return render(request, "administration/users.html", context)

# ---- CREATE NEW USER ----
def new_user(request):
    if not request.user.is_superuser:
        raise Http404("Page not found")
    
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        role = request.POST.get("role")
        list_role = request.POST.get("list_role", role)

        if username and role:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
            )
            user.profile.phone_number = phone_number
            user.profile.address = address
            user.profile.gender = gender
            user.profile.role = role.lower()
            user.profile.save()

            messages.success(request, f"{role.capitalize()} created successfully!")
           
            return redirect(f"/administration/users/?role={list_role.lower()}")
        else:
            messages.error(request, "Please provide complete information.")

    return redirect(f"/administration/users/?role=staff")

# ---- EDIT USER ----
def edit_user(request, id):
    if not request.user.is_superuser:
        raise Http404("Page not found")
    
    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        role = request.POST.get("role")
        list_role = request.POST.get("list_role", user.profile.role)

        # update
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.profile.phone_number = phone_number
        user.profile.address = address
        user.profile.gender = gender
        user.profile.role = role.lower()
        user.profile.save()
        user.save()

        messages.success(request, f"{role.capitalize()} updated successfully!")
        return redirect(f"/administration/users/?role={list_role.lower()}")

    return redirect(f"/administration/users/?role={user.profile.role}")

def tests(request):
    """
    Test list with search + pagination + delete + HTMX support
    """
    search = request.GET.get("search", "")

    # All tests, newest first
    tests_qs = MedicalTest.objects.all().order_by("-id")

    # Search filter
    if search:
        tests_qs = tests_qs.filter(
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
    paginator = Paginator(tests_qs, 2)  # 10 tests per page
    page_number = request.GET.get("page")
    tests_page = paginator.get_page(page_number)

    context = {
        "tests": tests_page,
        "paginator": paginator,
        "page_number": page_number,
        "search": search,
    }

    # HTMX request handling
    if request.headers.get("HX-Request") == 'true' and request.GET.get("type") == "search":
        return render(request, 'administration/htmx/test_search_result.html', context)
    elif request.headers.get("HX-Request") == 'true' and request.GET.get("type") == "pagination":
        return render(request, 'administration/htmx/test_table.html', context)
    else:
        return render(request, 'administration/tests.html', context)

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