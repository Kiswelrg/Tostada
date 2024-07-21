from django.shortcuts import render

# Create your views here.
def send_Msg(
        request,
        content,
        channel,
        user_from,
        user_mentioned = None,
        edited = False,
        tool_used = None,
        is_private = False,
    ):
    pass