from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from scr.adore.models.booking import Time, Comment
from scr.adore.models.region import *
from scr.adore.models.restaurant import *


@admin.register(Region)
class RegionModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "name")
    filter = ("name",)
    ordering = ("id",)
    search_fields = ("name",)


@admin.register(District)
class DistrictModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "name", "region")
    ordering = ("id",)
    search_fields = ("name",)


@admin.register(Mahalla)
class MahallaModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "name", "district")
    ordering = ("id",)
    search_fields = ("name",)


@admin.register(Service)
class ServiceModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "name", "image")
    ordering = ("id",)


@admin.register(Time)
class TimeModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "morning_time", "afternoon_time", "evening_time", "restaurant")
    ordering = ("id",)


@admin.register(Image)
class ImageModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "image", "restaurant")
    ordering = ("id",)


@admin.register(Comment)
class ImageModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "text", "user", "restaurant", "created_at")
    ordering = ("id",)


class RestaurantModelAdmin(admin.ModelAdmin):
    def get_address(self, obj):
        return str(obj.address)

    get_address.short_description = 'Address'

    def get_services(self, obj):
        return ', '.join([str(service) for service in obj.services.all()])

    get_services.short_description = 'Services'

    def get_times(self, obj):
        return ', '.join([str(time) for time in obj.time.all()])

    get_times.short_description = 'Times'

    list_display = ('id', 'name', 'phone', 'size_people', 'user', 'get_services', 'get_address', 'get_times')


admin.site.register(Restaurant, RestaurantModelAdmin)
