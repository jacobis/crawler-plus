# encoding: utf-8

from django.db import models

class ActivityObject(models.Model):
    json = models.TextField()
    

class CommentObject(models.Model):
    json = models.TextField()