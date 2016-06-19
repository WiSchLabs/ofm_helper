from django.contrib import admin

from users.models import OFMUser


@admin.register(OFMUser)
class VehicleClassAdmin(admin.ModelAdmin):
    list_display = ['username']
    search_fields = ['username']
