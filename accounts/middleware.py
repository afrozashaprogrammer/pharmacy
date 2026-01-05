import datetime
from django.utils import timezone
from django.conf import settings

class UpdateLastSeenMiddleware:
    """
    Middleware to update last_seen of authenticated users.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # যদি user authenticated হয়
        if request.user.is_authenticated:
            now = timezone.now()
            # আগের update থেকে 1 মিনিট পেরিয়ে গেলে update করো (performance reason)
            last_seen = getattr(request.user, 'last_login', None)
            if not last_seen or (now - last_seen).total_seconds() > 60:
                request.user.profile.last_seen = now
                request.user.profile.save(update_fields=['last_seen'])

        response = self.get_response(request)
        return response
