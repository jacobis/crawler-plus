# encoding: utf-8

from django.contrib import admin

from .models import ActivityObject, CommentObject

@admin.register(ActivityObject, CommentObject)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ['id']