# encoding: utf-8

from django.http import HttpResponse

import time
import json
import requests
from urlparse import urljoin

from .tasks import crawl_activities


def activities(request):
    request_get = request.GET.copy()
    crawl_activities(request_get)

    return HttpResponse('Request done!')


def key_list(request):
    object_type = request.GET.get('object_type')
    f = open("%s-result-%s.txt" % (object_type, time.strftime('%Y%m%d-%H%M')), 'w')
    
    if object_type == 'activity':
        object_querysets = ActivityJson.objects.all()
    elif object_type == 'comment':
        object_querysets = CommentJson.objects.all()

    for object_queryset in object_querysets:
        object_queryset = json.loads(object_queryset.json)
        try:
            keys = object_queryset['object']['actor'].keys()
            # keys = [attachment.keys() for attachment in attachments]
            f.write(str(keys) + '\n')
        except:
            pass

    f.close()
