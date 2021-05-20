from bocken.forms import AgreementForm
from import_export.admin import ImportExportModelAdmin


class AgreementAdmin(ImportExportModelAdmin):
    """Custom class for the admin pages for Agreement."""

    form = AgreementForm
    list_display = (
        'name', 'personnummer', 'phonenumber',
        'email', 'expires_colored'
    )
    search_fields = ['name', 'personnummer']
