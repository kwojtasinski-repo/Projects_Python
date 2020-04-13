from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Todo
from django.http import HttpResponseRedirect

# Create your views here.
def home(request):
    todo_items = Todo.objects.all().order_by("add_date")
    return render(request, 'site/index.html', {"todo_items": todo_items})

@csrf_exempt
def add_to_do(request):
    curr_date = timezone.now()
    txt = request.POST["content"]
    #print("Time {:%Y-%m-%d %H:%M:%S}".format(add_date))
    #print(content)
    created_obj = Todo.objects.create(content=txt, add_date=curr_date)
    #return render(request, 'site/index.html')
    return HttpResponseRedirect("/")

@csrf_exempt
def delete_todo(request, todo_id):
    #print(todo_id)
    print(Todo.objects.all())
    Todo.objects.get(id=todo_id).delete()
    return HttpResponseRedirect("/")