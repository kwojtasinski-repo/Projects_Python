from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', include('myapp.urls')),    # urls from myapp folder
    path('admin/', admin.site.urls),

    # Fallback for any other paths
    path('<path:anything>/', RedirectView.as_view(url='/', permanent=False))
]
