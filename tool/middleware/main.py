from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.urls import reverse
from urllib.parse import quote_plus

class LoginRequireMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
    # One-time configuration and initialization.

    def __call__(self,request):
        # Need to login
        except_list1 = []
        if request.path[:2] == '/i' and request.path not in except_list1:
            if not request.session.has_key("isLoggedIn") or not request.session["isLoggedIn"]:
                return HttpResponseRedirect(f"{reverse('user:sign-in')}?wish=" + quote_plus(request.path))

        # Need to be POST
        include_list2 = []
        for name in  include_list2:
            name = reverse('tool:' + name)
            if request.path == name  and request.method != "POST":
                raise Http404('Invalid request!')

        response = self.get_response(request)
        #something afterwards
        return response


            