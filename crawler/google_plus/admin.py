# encoding: utf-8

from django.contrib import admin

from .models import ActivityObject

class ActivityObjectAdmin(admin.ModelAdmin):
    list_display = ['id']

admin.site.register(ActivityObject, ActivityObjectAdmin)