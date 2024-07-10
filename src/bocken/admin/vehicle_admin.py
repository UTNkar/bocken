
from django.contrib.admin import ModelAdmin


class VehicleAdmin(ModelAdmin):
    """Custom class for the admin pages for Vehicle."""

    list_display = ("vehicle_name", "car", "bike", "vehicle_meter_start", "vehicle_meter_stop")
    list_filter = ['vehicle_name']
