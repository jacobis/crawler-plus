# encoding: utf-8

from django.contrib import admin

from .models import Actor, Attachment, ActivityObject, Activity, Comment, ActivityJson, CommentJson

@admin.register(ActivityJson, CommentJson)
class ObjectAdmin(admin.ModelAdmin):
    search_fields = ['json']

admin.site.register(Actor)
admin.site.register(Attachment)
admin.site.register(ActivityObject)
admin.site.register(Activity)
admin.site.register(Comment)
