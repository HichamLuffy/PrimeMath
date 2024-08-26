# from django.utils.deprecation import MiddlewareMixin
# from django.utils import timezone

# class UpdateLastActiveMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         if request.user.is_authenticated:
#             profile = request.user.profile
#             profile.last_active = timezone.now()
#             profile.save()
