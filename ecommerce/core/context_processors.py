from django.conf import settings

def payments_settings(request):
    return {
        "PAYMENTS_ENABLED": settings.PAYMENTS_ENABLED
    }
