from functools import wraps
from django.http import HttpResponse
from django.shortcuts import redirect

# If a user is logged in and tries to access the signup/login page, it wont redirect them to it, they will stay on the index page
# Else, the user will get returned to the signup/login page
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.username == "guest":
            return redirect("index")
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


# Sets only the allowed roles to access certain pages
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            request.has_access = group in allowed_roles
            return view_func(request, *args, **kwargs)

        return wrapper_func

    return decorator
