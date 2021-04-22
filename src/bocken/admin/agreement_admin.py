from django.contrib.admin import ModelAdmin
from bocken.forms import AgreementForm


class AgreementAdmin(ModelAdmin):
    """Custom class for the admin pages for Agreement."""

    form = AgreementForm
    list_display = (
        'name', 'personnummer', 'phonenumber',
        'email', 'expires_colored'
    )
    search_fields = ['name', 'personnummer']
