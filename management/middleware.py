from django.shortcuts import redirect
from django.urls import reverse

class CounterRedirectMiddleware:
    """
    Enforce role-based access for counter users.

    - Counter users are always redirected to /management/counter/
    - Counter users cannot access /management/ dashboard
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # Only for authenticated users
        if user.is_authenticated:
            profile = getattr(user, "profile", None)

            if profile and profile.role == "counter":
                counter_url = reverse("management:counter_dashboard")
                dashboard_url = reverse("management:dashboard")

                # ❌ Prevent counter from accessing main dashboard
                if request.path == dashboard_url:
                    return redirect(counter_url)

                # ✅ Optional: force counter to stay inside counter area
                if request.path.startswith("/management/") and request.path != counter_url:
                    return redirect(counter_url)

        return self.get_response(request)
