# encoding: utf-8

from .models import Actor, ActivityObject, Attachment, Activity, Comment


def store_actor(actor):
    actor_id = actor['id']
    actor = parse_actor(actor)
    try:
        actor.save()
    except:
        actor = Actor.objects.get(actor_id=actor_id)

    return actor


def parse_actor(actor):
    actor_id = actor['id']
    display_name = actor['displayName']
    url = actor['url']
    image = actor.get('image').get('url') if actor.get('image') else ''
    
    actor = Actor(actor_id=actor_id, display_name=display_name, url=url, image=image)

    return actor


def store_activity_object(activity_object):
    activity_object = parse_activity_object(activity_object)
    activity_object.save()

    return activity_object


def parse_activity_object(activity_object):
    object_type = activity_object['objectType']
    object_id = activity_object.get('id', '')
    content = activity_object['content']
    url = activity_object['url']
    plusoners = activity_object['plusoners']['totalItems']
    resharers = activity_object['resharers']['totalItems']

    activity_object = ActivityObject(object_type=object_type, object_id=object_id, content=content, url=url, plusoners=plusoners, resharers=resharers)

    return activity_object


def store_attachments(activity_object, activity_object_queryset):
    attachments = activity_object.get('attachments')
    
    if attachments:    
        for attachment in attachments:
            attachment = parse_attachments(attachment, activity_object_queryset)
            attachment.save()


def parse_attachments(attachment, activity_object_queryset):
    object_type = attachment['objectType']
    display_name = attachment.get('displayName', '')
    content = attachment.get('content', '')
    url = attachment['url']
    image = attachment.get('image').get('url') if attachment.get('image') else ''
    full_image = attachment.get('full_image').get('url') if attachment.get('full_image') else ''
    embed = attachment.get('embed').get('url') if attachment.get('embed') else ''

    attachment = Attachment(activity_object=activity_object_queryset, object_type=object_type, display_name=display_name, content=content, url=url, image=image, full_image=full_image, embed=embed)

    return attachment


def parse_activity(activity, actor, activity_object):
    kind = activity['kind']
    title = activity['title']
    published = activity['published']
    updated = activity['updated']
    activity_id = activity['id']
    url = activity['url']
    verb = activity['verb']
    annotation = activity.get('annotation', '')

    activity = Activity(kind=kind, title=title, published=published, updated=updated, activity_id=activity_id, url=url, actor=actor, verb=verb, activity_object=activity_object, annotation=annotation)

    return activity


def parse_comment(activity, comment, actor):
    activity = activity
    kind = comment['kind']
    verb = comment['verb']
    comment_id = comment['id']
    published = comment['published']
    updated = comment['updated']
    actor = actor
    content = comment['object']['content']
    self_link = comment['selfLink']
    plusoners = comment['plusoners']['totalItems']

    comment = Comment(activity=activity, kind=kind, verb=verb, comment_id=comment_id, published=published, updated=updated, actor=actor, content=content, self_link=self_link, plusoners=plusoners)

    return comment