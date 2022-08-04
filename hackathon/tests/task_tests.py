from datetime import datetime

from django.conf import settings
from django.test import TestCase, override_settings
import responses
from unittest.mock import patch, Mock

from accounts.models import Organisation, CustomUser as User
from hackathon.models import Hackathon
from hackathon.tasks import create_new_slack_channel


class TaskTests(TestCase):
    def setUp(self):
        organisation = Organisation.objects.create()
        self.user = User.objects.create(
            username="U213123_T123123",
            slack_display_name="bob",
            organisation=organisation,
        )
        self.hackathon = Hackathon.objects.create(
            created_by=self.user,
            display_name="hacktest",
            description="lorem ipsum",
            start_date=f'{datetime.now()}',
            end_date=f'{datetime.now()}')
        self.hackathon.channel_admins.add(self.user)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_create_new_slack_channel(self):
        channel_id = 'CH123123'
        responses.add(
            responses.POST, 'https://slack.com/api/conversations.create',
            json={'ok': True, 'channel': {'id': channel_id}}, status=200)
        responses.add(
            responses.POST, 'https://slack.com/api/conversations.invite',
            json={'ok': True}, status=200)
        create_new_slack_channel.apply_async(args=[
            self.hackathon.id, self.user.username])

        import time; time.sleep(3)
        self.assertEquals(
            self.hackathon.channel_url,
            f'https://{settings.SLACK_WORKSPACE}.slack.com/archives/{channel_id}')
