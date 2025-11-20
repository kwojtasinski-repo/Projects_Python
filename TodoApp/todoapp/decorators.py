from functools import wraps

from django.shortcuts import redirect


def post_only_redirect_home(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.method != "POST":
            return redirect("/")
        return view_func(request, *args, **kwargs)

    return wrapper
