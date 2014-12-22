# encoding: utf-8

from django.http import HttpResponse

import json
import requests
from urlparse import urljoin

from .models import ActivityObject


def activity_list(request):
    user_id = request.GET.get('user_id')
    collection = request.GET.get('collection', 'public')
    key = request.GET.get('key')

    url = 'people/%s/activities/%s' % (user_id, collection)
    params = {'key': key, 'maxResults': 100}
    
    items = []

    while True:
        response = google_api(url, params)
        next_page_token = response.get('nextPageToken', None)
        items += response.get('items')

        if next_page_token:
            params.update({'pageToken': next_page_token})
        else:
            break

    activity_objects = [ActivityObject(json="%s" % json.dumps(item)) for item in items]

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
