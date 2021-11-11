from django.contrib.admin import ModelAdmin


class JournalEntryAdmin(ModelAdmin):
    """Custom class for the admin pages for journal entry."""

    list_display = (
        'agreement', 'created', 'group',
        'meter_start', 'meter_stop', 'get_total_distance'
    )
    ordering = ('-meter_stop', )
    search_fields = [
        'agreement__name', 'agreement__personnummer', 'group__name'
    ]
    list_filter = ['group__name']
    autocomplete_fields = ['agreement']

    def get_readonly_fields(self, request, obj=None):
        """
        Only display created and get_total_distnace when editing.

        These fields should not be edited, they are there to provide extra
        information.
        """
        if obj:
            return ('created', 'get_total_distance')
        return ()
