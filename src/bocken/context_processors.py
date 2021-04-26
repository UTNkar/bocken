from .models import SiteSettings
from django.conf import settings


def sitesettings(request):  # noqa
    return {'sitesettings': SiteSettings.load()}


def klubbmastare_email(request):  # noqa
    return {
        'klubbmastare_email': settings.KLUBBMASTARE_EMAIL
    }
