import os

from django.conf import settings
from django.test import TestCase


def ImageTestCase(TestCase):
    setUp(self):
        img = os.join(settings.STATICFILES_DIRS[0], 'static', 'img',
                      'ci-logo.cvg')
        with open(
