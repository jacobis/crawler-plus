# encoding: utf-8

from django.http import HttpResponse

import json
import requests
from urlparse import urljoin

from .models import ActivityObject


def activity_list(request):
    user_id = request.GET.get('user_id', None)
    query = request.GET.get('query', None)
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

    item_list = []

    while True:
        response = google_api(url, params)
        next_page_token = response.get('nextPageToken', None)
        items = response.get('items')

        if next_page_token:
            params.update({'pageToken': next_page_token})
        if items:
            item_list += items
        else:
            break

    activity_objects = [ActivityObject(json="%s" % json.dumps(item)) for item in item_list]

    if activity_objects:
        ActivityObject.objects.bulk_create(activity_objects)

    result = "총 %s개의 Activity가 수집되었습니다." % len(activity_objects)

    return HttpResponse(result)


def google_api(url, params):
    GOOGLE_PLUS_URL = 'https://www.googleapis.com/plus/v1/'
    
    url = urljoin(GOOGLE_PLUS_URL, url)
    r = requests.get(url, params=params)
    print "Get page : '%s'" % r.url

    response = r.json()

    return response
