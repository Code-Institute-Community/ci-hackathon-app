from datetime import datetime

from django.conf import settings
from django.test import TestCase, override_settings
import responses
from unittest.mock import patch, Mock

from accounts.models import Organisation, CustomUser as User
from accounts.models import SlackSiteSettings
from hackathon.models import Hackathon
from hackathon.tasks import create_new_hackathon_slack_channel, \
                            invite_user_to_hackathon_slack_channel, \
                            kick_user_from_hackathon_slack_channel


class TaskTests(TestCase):
    def setUp(self):
        organisation = Organisation.objects.create()
        self.user = User.objects.create(
            username="U213123_T123123",
            slack_display_name="bob",
            organisation=organisation,
        )
        self.slack_site_settings = SlackSiteSettings.objects.create(
            remove_admin_from_channel=True
        )
        self.hackathon = Hackathon.objects.create(
            created_by=self.user,
            display_name="hacktest",
            description="lorem ipsum",
            start_date=f'{datetime.now()}',
            end_date=f'{datetime.now()}')
        self.hackathon.channel_admins.add(self.user)
    
    @responses.activate
    def test_create_new_hackathon_slack_channel(self):
        channel_id = 'CH123123'
        responses.add(
            responses.POST, 'https://slack.com/api/conversations.create',
            json={'ok': True, 'channel': {'id': channel_id}}, status=200)
        responses.add(
            responses.POST, 'https://slack.com/api/conversations.invite',
            json={'ok': True}, status=200)
        responses.add(
            responses.POST, 'https://slack.com/api/users.identity',
            json={'ok': True}, status=200)
        responses.add(
            responses.POST, 'https://slack.com/api/conversations.leave',
            json={'ok': True}, status=200)

        create_new_hackathon_slack_channel(self.hackathon.id, self.user.username)
        
        self.assertEquals(
            Hackathon.objects.first().channel_url,
            f'https://{settings.SLACK_WORKSPACE}.slack.com/archives/{channel_id}')
       
    @responses.activate
    def test_invite_user_to_channel(self):
        channel_id = 'CH123123'
        self.hackathon.channel_url = 'https://{settings.SLACK_WORKSPACE}.slack.com/archives/{channel_id}'
        self.hackathon.save()

        responses.add(
            responses.POST, 'https://slack.com/api/conversations.invite',
            json={'ok': True}, status=200)
        
        try:
            invite_user_to_hackathon_slack_channel(self.hackathon.id, self.user.id)
        except:
            raise Exception("Inviting user to channel failed")

    @responses.activate
    def test_kick_user_from_channel(self):
        channel_id = 'CH123123'
        self.hackathon.channel_url = 'https://{settings.SLACK_WORKSPACE}.slack.com/archives/{channel_id}'
        self.hackathon.save()

        responses.add(
            responses.POST, 'https://slack.com/api/conversations.kick',
            json={'ok': True}, status=200)

        try:
            kick_user_from_hackathon_slack_channel(self.hackathon.id, self.user.id)
        except:
            raise Exception("Kicking user from channel failed")
