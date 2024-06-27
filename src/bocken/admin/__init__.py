from bocken.models import (
    Admin, Agreement, JournalEntry, Report, JournalEntryGroup, Vehicle
)
from .agreement_admin import AgreementAdmin
from .journal_entry_admin import JournalEntryAdmin
from .journal_entry_group_admin import JournalEntryGroupAdmin
from .report_admin import ReportAdmin
from .vehicle_admin import VehicleAdmin
from .user_admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.models import Group


admin.site.register(Admin, UserAdmin)
admin.site.register(Agreement, AgreementAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(JournalEntry, JournalEntryAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(JournalEntryGroup, JournalEntryGroupAdmin)

admin.site.unregister(Group)

admin.site.site_header = _("Bocken Administration")
admin.site.site_title = _("Bocken Journal System")
