# encoding: utf-8

from django.db import models


class Actor(models.Model):
    actor_id = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=200)
    url = models.URLField(max_length=500)
    image = models.URLField(max_length=500, blank=True)


class ActivityObject(models.Model):
    object_type = models.CharField(max_length=30)
    object_id = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    url = models.URLField(max_length=500)
    plusoners = models.IntegerField()
    resharers = models.IntegerField()


class Attachment(models.Model):
    activity_object = models.ForeignKey(ActivityObject)
    object_type = models.CharField(max_length=30)
    display_name = models.CharField(max_length=500)
    content = models.TextField()
    url = models.URLField(max_length=500)
    image = models.URLField(max_length=500, blank=True)
    full_image = models.URLField(max_length=500, blank=True)
    embed = models.URLField(max_length=500, blank=True)


class Activity(models.Model):
    kind = models.CharField(max_length=50)
    title = models.CharField(max_length=500)
    published = models.DateTimeField()
    updated = models.DateTimeField()
    activity_id = models.CharField(max_length=100, unique=True)
    url = models.URLField(max_length=500)
    actor = models.ForeignKey(Actor)
    verb = models.CharField(max_length=30)
    activity_object = models.ForeignKey(ActivityObject)
    annotation = models.TextField(blank=True)


class Comment(models.Model):
    activity = models.ForeignKey(Activity)
    kind = models.CharField(max_length=50)
    verb = models.CharField(max_length=30)
    comment_id = models.CharField(max_length=100, unique=True)
    published = models.DateTimeField()
    updated = models.DateTimeField()
    actor = models.ForeignKey(Actor)
    content = models.TextField()
    self_link = models.URLField(max_length=500)
    plusoners = models.IntegerField()
        

class ActivityJson(models.Model):
    object_id = models.CharField(max_length=100, unique=True)
    json = models.TextField()
    comment_total_items = models.IntegerField()
    is_crawled = models.BooleanField(default=False)
    

class CommentJson(models.Model):
    activity_id = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    json = models.TextField()
    is_crawled = models.BooleanField(default=False)

    unique_together = ("activity_id", "object_id")