# encoding: utf-8

from django.db import models


class Actor(models.Model):
    actor_id = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100)
    url = models.URLField()
    image = models.URLField(blank=True)


class Attachment(models.Model):
    object_type = models.CharField(max_length=30)
    display_name = models.CharField(max_length=100)
    content = models.TextField()
    url = models.URLField()
    image = models.URLField(blank=True)
    full_image = models.URLField(blank=True)
    embed = models.URLField(blank=True)


class ActivityObject(models.Model):
    object_type = models.CharField(max_length=30)
    object_id = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    url = models.URLField()
    plusoners = models.IntegerField()
    resharers = models.IntegerField()
    attachment = models.OneToOneField(Attachment, blank=True, null=True)


class Activity(models.Model):
    kind = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    published = models.DateTimeField()
    updated = models.DateTimeField()
    activity_id = models.CharField(max_length=100, unique=True)
    url = models.URLField()
    actor = models.ForeignKey(Actor)
    verb = models.CharField(max_length=30)
    activity_object = models.ForeignKey(ActivityObject)
    annotation = models.TextField(blank=True)


class Comment(models.Model):
    activity_object = models.ForeignKey(ActivityObject)
    kind = models.CharField(max_length=50)
    verb = models.CharField(max_length=30)
    comment_id = models.CharField(max_length=100, unique=True)
    published = models.DateTimeField()
    updated = models.DateTimeField()
    actor = models.ForeignKey(Actor)
    content = models.TextField()
    self_link = models.URLField()
    plusoners = models.IntegerField()


class ActivityJson(models.Model):
    json = models.TextField()
    

class CommentJson(models.Model):
    json = models.TextField()