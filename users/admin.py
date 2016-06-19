from django.contrib import admin

from users.models import OFMUser


@admin.register(OFMUser)
class OFMUserAdmin(admin.ModelAdmin):
    exclude = ('ofm_password',)
