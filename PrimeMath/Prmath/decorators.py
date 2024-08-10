from django.http import HttpResponseForbidden

def student_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if hasattr(request.user, 'profile') and request.user.profile.role == 'student':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You must be a student to access this page.")
    return wrapper_func

def teacher_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if hasattr(request.user, 'profile') and request.user.profile.role == 'teacher':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You must be a teacher to access this page.")
    return wrapper_func
