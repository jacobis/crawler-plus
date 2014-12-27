from __future__ import absolute_import

from celery import task

from .api import activities, comments

@task
def crawl_activities(request_get):
    fetch_activities_json.delay(request_get)


@task
def fetch_activities_json(request_get):
    activity_objects = activities(request_get)
    activity_ids = [activity_object.object_id for activity_object in activity_objects]

    for activity_id in activity_ids:
        request_get.update({'activity_id': activity_id})
        fetch_comments_json.delay(request_get)
    

@task(ignore_result=True)
def fetch_comments_json(request_get):
    comments(request_get)