from django.urls import path, re_path
from . import views
from django.views.generic.base import RedirectView

urlpatterns=[
  path('', views.home, name='home'),
  path('addtodo/',views.add_todo, name='add_todo'),
  path('delete_todo/<int:todo_id>/', views.delete_todo, name='delete_todo'),

  # Fallback for any other paths
  re_path(r'^.*$', RedirectView.as_view(url='/', permanent=False))
]
