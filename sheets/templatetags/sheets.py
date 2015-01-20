from __future__ import unicode_literals

from django import template
from django.conf import settings
from django.core.cache import cache
from django.utils.encoding import force_str, force_text
from django.utils.functional import cached_property

import csv
import logging
import requests

logger = logging.getLogger(__name__)
register = template.Library()

gdocs_format = \
    'https://docs.google.com/spreadsheets/d/{key}/export?format=csv&id={key}'

CACHE_TIMEOUT = getattr(settings, 'SHEETS_CACHE_TIMEOUT', 300)
CACHE_KEY = 'django-sheets-{key}'


class Sheet(object):

    def __init__(self, key):
        self.key = key

    @cached_property
    def data(self):
        response = requests.get(gdocs_format.format(key=self.key))
        response.raise_for_status()
        reader = csv.reader(
            force_str(response.content).splitlines(),
            delimiter=str(','),
            quotechar=str('"'),
            quoting=csv.QUOTE_MINIMAL,
        )
        return [[(value if type(value), float) else force_str(value))
            for value in rows] for rows in reader]

    def __len__(self):
        return len(self.data)

    def headers(self):
        return self.data[0] if self.data else [] 

    def rows(self):
        return self.data[1:] if len(self) > 1 else []

    def next(self):
        for row in self.data:
            yield row


class ExplicitNone:
    pass


@register.assignment_tag(name='csv')
def csv_tag(key):
    if not key:
        raise RuntimeError('Sheet key not supplied')

    cache_enabled = not getattr(settings, 'SHEETS_CACHE_DISABLED', False)

    if cache_enabled:
        cache_key = CACHE_KEY.format(key=key)
        cached_output = cache.get(cache_key)
        if cached_output is not None:
            return cached_output

    sheet = Sheet(key)

    if cache_enabled:
        cache.set(cache_key, sheet, CACHE_TIMEOUT)

    return sheet
