from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles=None):
    """Decorator to restrict access based on user role."""
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                messages.error(request, "You must be logged in.")
                return redirect("login")

            # Check if user has a profile and role
            if hasattr(user, "userprofile") and user.userprofile.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You are not authorized to view this page.")
                return redirect("user_dashboard")
        return wrapper
    return decorator
