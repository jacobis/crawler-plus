# encoding: utf-8

from django.http import HttpResponse

import djqscsv
import time
import json
import requests
from urlparse import urljoin

from .models import Activity
from .tasks import crawl_activities, fetch_to_json, parse_to_object


def activities(request):
    request_get = request.GET.copy()
    crawl_activities(request_get)

    return HttpResponse('Crawl activity request done!')


def fetch_json(request):
    request_get = request.GET.copy()
    fetch_to_json(request_get)

    return HttpResponse('Fetch to json request done!')


def parse_object(request):
    parse_to_object()

    return HttpResponse('Parse to object request done!')


def activities_export_to_csv(request, actor_id):
    activities = Activity.objects.filter(actor__actor_id=actor_id)
    activities = activities.values('id', 'kind', 'published', 'updated', 'activity_id', 'url', 'actor__actor_id', 'actor__display_name', 'actor__url', 'actor__image', 'verb', 'activity_object__object_type', 'activity_object__object_id', 'activity_object__content', 'activity_object__url', 'activity_object__plusoners', 'activity_object__resharers', 'annotation')
    
    return djqscsv.render_to_csv_response(activities)