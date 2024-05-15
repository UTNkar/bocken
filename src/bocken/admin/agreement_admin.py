from bocken.forms import AgreementForm
from import_export.admin import ImportExportModelAdmin
from bocken.models.agreement import AgreementResource


class AgreementAdmin(ImportExportModelAdmin):
    """Custom class for the admin pages for Agreement."""

    resource_class = AgreementResource
    form = AgreementForm
    list_display = (
        'name', 'personnummer', 'phonenumber',
        'agreement_hornet_type', 'agreement_bocken_type',
        'email', 'expires_colored'
    )
    search_fields = ['name', 'personnummer']
