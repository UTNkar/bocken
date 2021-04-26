from django.contrib import admin
from bocken.models import (
    Admin, Agreement, JournalEntry, Report, JournalEntryGroup
)
from .agreement_admin import AgreementAdmin
from .journal_entry_admin import JournalEntryAdmin
from .journal_entry_group_admin import JournalEntryGroupAdmin
from .report_admin import ReportAdmin
from .user_admin import UserAdmin
from django.contrib.auth.models import Group

admin.site.register(Admin, UserAdmin)
admin.site.register(Agreement, AgreementAdmin)
admin.site.register(JournalEntry, JournalEntryAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(JournalEntryGroup, JournalEntryGroupAdmin)

# Hide groups from the admin view since they are not used
admin.site.unregister(Group)
