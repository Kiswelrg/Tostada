from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.urls import reverse
from urllib.parse import quote_plus

class LoginRequireMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
    # One-time configuration and initialization.

    def __call__(self,request):
        # Need to login
        except_list1 = ['/i/toolapi/']
        if request.path[:2] == '/i':
            should_exclude = False
            for item in except_list1:
                if len(item) <= len(request.path) and item == request.path[:len(item)]:
                    should_exclude = True
                    break
            if not should_exclude and (not request.session.has_key("isLoggedIn") or not request.session["isLoggedIn"]):
                return HttpResponseRedirect(f"{reverse('account:sign-in')}?wish=" + quote_plus(request.path))

        # Need to be POST
        include_list2 = []
        for name in  include_list2:
            name = reverse('tool:' + name)
            if request.path == name  and request.method != "POST":
                raise Http404('Invalid request!')

        response = self.get_response(request)
        #something afterwards
        return response


            