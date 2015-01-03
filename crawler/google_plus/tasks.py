# encoding: utf-8

from __future__ import absolute_import

import json
from celery import task, chain
from celery.exceptions import SoftTimeLimitExceeded

from .models import Actor, Activity, ActivityObject, ActivityJson, CommentJson
from .api import activities, comments
from .parse import parse_save_actor, parse_save_activity_object, parse_save_attachment, parse_save_activity, parse_save_comment


@task
def crawl_activities(request_get):
    fetch_to_json.apply_async((request_get,), link=parse_to_object.si())


@task
def fetch_to_json(request_get):
    activity_jsons = fetch_activity_jsons(request_get)
    
    if activity_jsons:
        activities = [activity_json.object_id for activity_json in activity_jsons]

        for activity in activities:
            request_get.update({'activity_id':activity})
            fetch_comments_json.delay(request_get)


def fetch_activity_jsons(request_get):
    activity_jsons = activities(request_get)
    
    return activity_jsons
    

@task
def fetch_comments_json(request_get):
    comments(request_get)


@task
def parse_to_object():
    activity_parse_to_object.apply_async((), link=comment_parse_to_object.si())


@task
def activity_parse_to_object():
    activity_jsons = ActivityJson.objects.filter(is_crawled=False)
    for activity_json in activity_jsons:
        activity = json.loads(activity_json.data)
        activity_object_maker.delay(activity) 

    activity_jsons.update(is_crawled=True)


@task
def comment_parse_to_object():
    comment_jsons = CommentJson.objects.filter(is_crawled=False)
    for comment_json in comment_jsons:
        comment = json.loads(comment_json.data)
        comment_object_maker.delay(comment)

    comment_jsons.update(is_crawled=True)


@task
def activity_object_maker(activity):
    activity_id = chain(
        store_actor.s(activity.get('actor')),
        store_activity_object.s(activity.get('object')),
        store_attachments.s(activity.get('object')),
        store_activity.s(activity)
    ).apply_async()
    
    return activity_id


@task
def comment_object_maker(comment):
    comment_id = chain(
        store_actor.s(comment.get('actor')),
        store_comment.s(comment)
    ).apply_async()
    
    return comment_id


@task
def store_actor(actor):
    actor = parse_save_actor(actor)
    data = {'actor_id': actor.id}
    
    return data


@task
def store_activity_object(data, activity_object):
    activity_object = parse_save_activity_object(activity_object)
    data['activity_object_id'] = activity_object.id
    
    return data


@task
def store_attachments(data, activity_object):
    attachments = activity_object.get('attachments')
    activity_object = ActivityObject.objects.get(id=data['activity_object_id'])

    if attachments:
        for attachment in attachments:
            parse_save_attachment(attachment, activity_object)
    
    return data


@task(time_limit=10)
def store_activity(data, activity):
    try:
        actor = Actor.objects.get(id=data['actor_id'])
        activity_object = ActivityObject.objects.get(id=data['activity_object_id'])
        parse_save_activity(actor, activity_object, activity)
    except SoftTimeLimitExceeded:
        raise self.retry(countdown=5)


@task(bind=True, time_limit=10)
def store_comment(self, data, comment):
    try:
        activity = Activity.objects.get(activity_id=comment.get('id').split('.')[0])
        actor = Actor.objects.get(id=data['actor_id'])
        parse_save_comment(activity, actor, comment)

    except (SoftTimeLimitExceeded, Exception):
        raise self.retry(countdown=5)