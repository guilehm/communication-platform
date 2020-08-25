from django.contrib import admin
from communication.core.models import Addressee, Scheduling


@admin.register(Addressee)
class AddresseeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile_number', 'device_token')
    list_filter = ('date_added', 'date_changed')
    search_fields = ('name', 'email', 'mobile_number', 'device_token')
    date_hierarchy = 'date_added'


@admin.register(Scheduling)
class SchedulingAdmin(admin.ModelAdmin):
    list_display = ('id', 'addressee', 'type', 'sending_time', 'sent')
    list_filter = ('sent', 'type')
    search_fields = ('message', 'addressee__name', 'addressee__email')
    date_hierarchy = 'date_added'
    readonly_fields = ('sent',)
