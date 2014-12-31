# encoding: utf-8

from __future__ import absolute_import

import time
from json import loads
from celery import task, chain

from .models import Activity, ActivityJson, CommentJson
from .api import activities, comments
from .parse import store_actor, store_activity_object, store_attachments, parse_activity, parse_comment


@task(ignore_result=True)
def crawl_activities(request_get):
    fetch_to_json.apply_async((request_get,), link=parse_to_object.s(direct=False))


@task
def fetch_to_json(request_get):
    activities_json = fetch_activities_json(request_get)
    activities = [{'activity_id':activity_json.object_id, 'comment_total_items':activity_json.comment_total_items} for activity_json in activities_json]
    request_get.update({'activities':activities})

    for activity in activities:
        request_get.update({'activity_id':activity['activity_id']})
        fetch_comments_json.delay(request_get)

    return request_get


def fetch_activities_json(request_get):
    activities_json = activities(request_get)
    
    return activities_json
    

@task(ignore_result=True)
def fetch_comments_json(request_get):
    comments(request_get)


@task(ignore_result=True)
def parse_to_object(request_get, direct=True):
    if direct:
        activities = request_get.get('activities').split(',')
        for activity in activities:
            request_get.update({'activity_id':activity, 'comment_total_items':ActivityJson.objects.get(object_id=activity).comment_total_items})
            
            store_activity.apply_async((request_get,), link=store_comment.s())

    else:
        activities = request_get.get('activities')
        for activity in activities:
            request_get.update({'activity_id':activity['activity_id'], 'comment_total_items':activity['comment_total_items']})
            
            store_activity.apply_async((request_get,), link=store_comment.s())

    
@task
def store_activity(request_get):
    activity_id = request_get.get('activity_id')
    activity = loads(ActivityJson.objects.get(object_id=activity_id).json)

    actor = store_actor(activity.get('actor'))
    activity_object = store_activity_object(activity.get('object'))
    store_attachments(activity.get('object'), activity_object)
    activity = parse_activity(activity, actor, activity_object)
    activity.save()

    return request_get


@task(ignore_result=True)
def store_comment(request_get):
    if request_get.get('comment_total_items') > 0:
        activity_id = request_get.get('activity_id')
        activity = Activity.objects.get(activity_id=activity_id)
        comments = CommentJson.objects.filter(activity_id=activity_id)

        for comment in comments:
            comment = loads(comment.json)

            actor = store_actor(comment.get('actor'))
            comment = parse_comment(activity, comment, actor)
            comment.save()