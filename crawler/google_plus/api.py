# encoding: utf-8

import json
import requests
from urlparse import urljoin

from .models import ActivityObject, ActivityJson, CommentJson


def activities(request_get):
    user_id = request_get.get('user_id')
    query = request_get.get('query')
    collection = request_get.get('collection', 'public')
    language = request_get.get('language', 'ko')
    key = request_get.get('key')

    if user_id:
        url = 'people/%s/activities/%s' % (user_id, collection)
        params = {'maxResults': 100}
    elif query and language:
        url = 'activities'
        params = {'query': query, 'maxResults': 20, 'language': language}

    params.update({'key': key})

    item_list = items(url, params)

    activity_objects = [ActivityJson(object_id=item['id'], json="%s" % json.dumps(item)) for item in item_list if not ActivityJson.objects.filter(object_id=item['id']).exists()]

    if activity_objects:
        activity_objects = ActivityJson.objects.bulk_create(activity_objects)

    return activity_objects


def comments(request_get):
    activity_id = request_get.get('activity_id')
    key = request_get.get('key')

    url = 'activities/%s/comments' % activity_id
    params = {'maxResults': 500}

    params.update({'key': key})

    item_list = items(url, params)

    comment_objects = [CommentJson(activity_id=activity_id, object_id=item['id'], json="%s" % json.dumps(item)) for item in item_list if not CommentJson.objects.filter(activity_id=activity_id, object_id=item['id']).exists()]

    if comment_objects:
        CommentJson.objects.bulk_create(comment_objects)

    return comment_objects


def items(url, params):
    item_list = []

    while True:
        response = google_api(url, params)
        next_page_token = response.get('nextPageToken', None)
        items = response.get('items')

        if items:
            item_list += items

        if items and next_page_token:
            params.update({'pageToken': next_page_token})
        else:
            break

    return item_list


def google_api(url, params):
    GOOGLE_PLUS_URL = 'https://www.googleapis.com/plus/v1/'
    
    url = urljoin(GOOGLE_PLUS_URL, url)
    r = requests.get(url, params=params)
    print "Get page : '%s'" % r.url

    response = r.json()

    return response