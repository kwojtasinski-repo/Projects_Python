from django.urls import path
from . import views

urlpatterns=[
  path('', views.home, name='home'),
  path('addtodo/',views.add_to_do),
  path('delete_todo/<int:todo_id>/', views.delete_todo)
]