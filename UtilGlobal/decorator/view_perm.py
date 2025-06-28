from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from functools import wraps


def require_login(view_func):
    """
    Decorator that can be used for both views and consumers.
    For views, it redirects to login page.
    For consumers, it raises PermissionDenied.
    """
    @wraps(view_func)
    def wrapper(request_or_self, *args, **kwargs):
        # Check if this is a consumer (has 'user' attribute) or a view (first param is request)
        if hasattr(request_or_self, 'user'):
            # This is a consumer
            if request_or_self.user.is_authenticated:
                return view_func(request_or_self, *args, **kwargs)
            raise PermissionDenied
        else:
            # This is a view - use Django's login_required decorator
            return login_required(view_func)(request_or_self, *args, **kwargs)
    return wrapper