# encoding: utf-8

from django.db import models


class Actor(models.Model):
    actor_id = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=200)
    url = models.TextField()
    image = models.TextField(blank=True)


class ActivityObject(models.Model):
    object_type = models.CharField(max_length=30)
    object_id = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    url = models.TextField()
    plusoners = models.IntegerField()
    resharers = models.IntegerField()


class Attachment(models.Model):
    activity_object = models.ForeignKey(ActivityObject)
    object_type = models.CharField(max_length=30)
    display_name = models.TextField()
    content = models.TextField()
    url = models.TextField()
    image = models.TextField(blank=True)
    full_image = models.TextField(blank=True)
    embed = models.TextField(blank=True)


class Activity(models.Model):
    kind = models.CharField(max_length=50)
    title = models.CharField(max_length=500)
    published = models.DateTimeField()
    updated = models.DateTimeField()
    activity_id = models.CharField(max_length=100, unique=True)
    url = models.TextField()
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
    self_link = models.TextField()
    plusoners = models.IntegerField()
        

class ActivityJson(models.Model):
    object_id = models.CharField(max_length=100, unique=True)
    data = models.TextField()
    is_crawled = models.BooleanField(default=False)
    

class CommentJson(models.Model):
    activity_id = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    data = models.TextField()
    is_crawled = models.BooleanField(default=False)

    unique_together = ("activity_id", "object_id")