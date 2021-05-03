from django.contrib.admin import ModelAdmin


class AgreementAdmin(ModelAdmin):
    """Custom class for the admin pages for Agreement."""

    list_display = (
        'name', 'personnummer', 'phonenumber',
        'email', 'expires_colored'
    )
    search_fields = ['name', 'personnummer']
