from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from .decorators import post_only_redirect_home
from .models import Todo


def home(request: HttpRequest) -> HttpResponse:
    todo_items = Todo.objects.all().order_by("add_date")
    return render(request, "site/index.html", {"todo_items": todo_items})


@post_only_redirect_home
def add_todo(request: HttpRequest) -> HttpResponse:
    txt = request.POST.get("content", "").strip()
    if txt:
        Todo.objects.create(content=txt, add_date=timezone.now())

    return redirect("/")


@post_only_redirect_home
def delete_todo(_: HttpRequest, todo_id: int) -> HttpResponse:
    Todo.objects.filter(id=todo_id).delete()
    return redirect("/")
