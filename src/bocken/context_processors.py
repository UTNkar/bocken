from django.conf import settings


def klubbmastare_email(request):  # noqa
    return {
        'klubbmastare_email': settings.KLUBBMASTARE_EMAIL
    }
