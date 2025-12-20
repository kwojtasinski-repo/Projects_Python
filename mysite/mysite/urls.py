from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),

    # Fallback for any other paths
    path("", RedirectView.as_view(url="polls/", permanent=False)),
    path('<path:anything>/', RedirectView.as_view(url='polls/', permanent=False))
]
