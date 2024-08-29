# Prmath/middleware.py

from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from ...Prmath.models import Profile

class UpdateLastSeenMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            now = timezone.now()
            updated = Profile.objects.filter(user=request.user).update(last_seen=now)
            print("##########update_last activite#######")
            print(f"Middleware: Updated last_seen for user {request.user.username} to {now}, Update count: {updated}")
            print("#################")
        return None