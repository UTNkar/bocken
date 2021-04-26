from django.contrib.admin import ModelAdmin


class JournalEntryGroupAdmin(ModelAdmin):
    """Custom class for the admin pages for JournalEntryGroup."""

    list_display = ("name", "main_group")
    ordering = ("main_group", "name")
    list_filter = ['main_group']
