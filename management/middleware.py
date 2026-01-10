from django.shortcuts import redirect
from django.urls import reverse

class CounterRedirectMiddleware:
    """
    Counter users:
    - Cannot access main management dashboard
    - Can access /management/counter/* URLs freely
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated:
            profile = getattr(user, "profile", None)

            if profile and profile.role == "counter":
                dashboard_url = reverse("management:dashboard")
                counter_prefix = "/management/counter/"

                # ❌ Block main dashboard only
                if request.path == dashboard_url:
                    return redirect(reverse("management:counter_dashboard"))

                # ✅ Allow all counter URLs
                if request.path.startswith(counter_prefix):
                    return self.get_response(request)

        return self.get_response(request)
