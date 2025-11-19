from django.shortcuts import render
from django.utils import timezone
from .models import Todo
from .decorators import post_only_redirect_home
from django.http import HttpResponseRedirect

def home(request):
    todo_items = Todo.objects.all().order_by("add_date")
    return render(request, 'site/index.html', {"todo_items": todo_items})

@post_only_redirect_home
def add_todo(request):
    curr_date = timezone.now()
    txt = request.POST.get("content")
    if txt:
        Todo.objects.create(content=txt, add_date=curr_date)

    return HttpResponseRedirect("/")

@post_only_redirect_home
def delete_todo(_, todo_id):
    Todo.objects.get(id=todo_id).delete()
    return HttpResponseRedirect("/")
