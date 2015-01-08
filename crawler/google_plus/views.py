# encoding: utf-8

from django.http import HttpResponse

import time
import json
import requests
from urlparse import urljoin

from .models import Activity
from .tasks import crawl_activities, fetch_to_json, parse_to_object, export_activities_csv


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


def activities_csv(request):
    request_get = request.GET.copy()
    response = export_activities_csv(request_get)
    
    return response
    # return HttpResponse('Activities export to CSV request done!')