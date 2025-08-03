from django.conf import settings


def union_house_manager_email(request):
    return {
        'union_house_manager_email': settings.UNION_HOUSE_MANAGER_EMAIL
    }
