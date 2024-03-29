from django.http import HttpResponseForbidden

def account_login(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Add your custom logic here
        if not request.session.has_key('isLoggedIn') or not request.session.has_key('username') or not request.session['isLoggedIn']:
            return HttpResponseForbidden("You are not allowed to access this page")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

