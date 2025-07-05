from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps


def require_login(view_func):
    """
    Decorator that can be used for both views and consumers.
    For views, it redirects to login page.
    For consumers, it raises PermissionDenied.
    """
    @wraps(view_func)
    def wrapper(request_or_self, *args, **kwargs):
        # Check if this is a consumer or a view by checking the type
        # Views receive HttpRequest objects, consumers are instances of consumer classes
        from django.http import HttpRequest
        
        if isinstance(request_or_self, HttpRequest):
            print(type(request_or_self), 'View!')
            # This is a view - check authentication and redirect to custom login
            if request_or_self.user.is_authenticated:
                return view_func(request_or_self, *args, **kwargs)
            else:
                # Custom redirect to account login
                login_url = reverse('account:login')
                next_url = request_or_self.get_full_path()
                return redirect(f'{login_url}?next={next_url}')
        else:
            print(type(request_or_self), 'Consumer!')
            # This is a consumer
            if request_or_self.user.is_authenticated:
                return view_func(request_or_self, *args, **kwargs)
            raise PermissionDenied
    return wrapper