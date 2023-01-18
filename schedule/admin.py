from django.contrib import admin
from django.contrib.admin import ModelAdmin

from schedule.models import Setup


class SetupAdmin(ModelAdmin):
    list_display = ('id', 'title', 'status', 'created_at', 'task')


admin.site.register(Setup, SetupAdmin)
