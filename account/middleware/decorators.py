from django.http import HttpResponseForbidden

def account_login(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Simplified to use Django's built-in authentication
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You are not allowed to access this page")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

