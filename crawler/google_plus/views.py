# encoding: utf-8

from django.http import HttpResponse

import time
import json
import requests
from urlparse import urljoin

from .models import ActivityObject, CommentObject


def activity_list(request):
    user_id = request.GET.get('user_id')
    query = request.GET.get('query')
    collection = request.GET.get('collection', 'public')
    language = request.GET.get('language', 'ko')
    key = request.GET.get('key')

    if user_id:
        url = 'people/%s/activities/%s' % (user_id, collection)
        params = {'maxResults': 100}
    elif query and language:
        url = 'activities'
        params = {'query': query, 'maxResults': 20, 'language': language}

    params.update({'key': key})

    item_list = get_item_list(url, params)

    activity_objects = [ActivityObject(json="%s" % json.dumps(item)) for item in item_list]

    if activity_objects:
        ActivityObject.objects.bulk_create(activity_objects)

    result = "총 %s개의 Activity가 수집되었습니다." % len(activity_objects)

    return HttpResponse(result)


def comment_list(request):
    activity_id = request.GET.get('activity_id')
    key = request.GET.get('key')

    url = 'activities/%s/comments' % activity_id
    params = {'maxResults': 500}

    params.update({'key': key})

    item_list = get_item_list(url, params)

    comment_objects = [CommentObject(json="%s" % json.dumps(item)) for item in item_list]

    if comment_objects:
        CommentObject.objects.bulk_create(comment_objects)

    result = "총 %s개의 Comment가 수집되었습니다." % len(comment_objects)

    return HttpResponse(result)


def get_item_list(url, params):
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


def key_list(request):
    object_type = request.GET.get('object_type')
    f = open("%s-result-%s.txt" % (object_type, time.strftime('%Y%m%d-%H%M')), 'w')
    
    if object_type == 'activity':
        object_querysets = ActivityObject.objects.all()
    elif object_type == 'comment':
        object_querysets = CommentObject.objects.all()

    for object_queryset in object_querysets:
        object_queryset = json.loads(object_queryset.json)
        f.write(str(object_queryset['object'].keys()) + '\n')

    f.close()
