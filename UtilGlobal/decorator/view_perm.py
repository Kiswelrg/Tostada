from django.core.exceptions import PermissionDenied


def require_login(consumer_func):
    def wrapper(self, *args, **kwargs):
        if self.user.is_authenticated:
            return consumer_func(self, *args, **kwargs)
        raise PermissionDenied
    return wrapper