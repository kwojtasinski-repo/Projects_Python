from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', include('myapp.urls')),    # urls from myapp folder
    path('admin/', admin.site.urls)
]

handler404 = "myapp.views.not_found"
