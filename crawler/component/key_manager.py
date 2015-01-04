# encoding: utf-8

from .models import KeyManager

import random


def get_key(service):
    keys = KeyManager.objects.filter(service=service, is_active=False).values_list('key', flat=True)
    key = random.choice(keys)

    return key