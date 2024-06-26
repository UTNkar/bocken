
from django.contrib.admin import ModelAdmin


class VehicleAdmin(ModelAdmin):
    """Custom class for the admin pages for JournalEntryGroup."""

    list_display = ("vehicle_type", "vehicle_meter_start", "vehicle_meter_stop")
    list_filter = ['vehicle_type']
