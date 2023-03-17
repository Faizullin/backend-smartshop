from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def group_required(group_names):
    """
    Decorator that checks if the user belongs to at least one of the specified
    groups. If not, redirects to the login page or raises a PermissionDenied
    exception, depending on the `login_url` and `raise_exception` arguments.
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return wrapper
    return decorator