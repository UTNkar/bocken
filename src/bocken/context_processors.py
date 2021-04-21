from .models import SiteSettings


def sitesettings(request):  # noqa
    return {'sitesettings': SiteSettings.load()}
