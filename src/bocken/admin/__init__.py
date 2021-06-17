from django.contrib.admin import AdminSite
from bocken.models import (
    Admin, Agreement, JournalEntry, Report, JournalEntryGroup
)
from .agreement_admin import AgreementAdmin
from .journal_entry_admin import JournalEntryAdmin
from .journal_entry_group_admin import JournalEntryGroupAdmin
from .report_admin import ReportAdmin
from .user_admin import UserAdmin
from django.utils.translation import gettext_lazy as _


class BockenAdminSite(AdminSite):
    """Override the default admin site."""

    site_header = _("Bocken Administration")
    site_title = _("Bocken Journal System")


admin_site = BockenAdminSite(name='bocken')

admin_site.register(Admin, UserAdmin)
admin_site.register(Agreement, AgreementAdmin)
admin_site.register(JournalEntry, JournalEntryAdmin)
admin_site.register(Report, ReportAdmin)
admin_site.register(JournalEntryGroup, JournalEntryGroupAdmin)
