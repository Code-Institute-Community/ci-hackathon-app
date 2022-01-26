from allauth.socialaccount.tests import OAuth2TestsMixin
from allauth.tests import MockedResponse, TestCase
from allauth.socialaccount.tests import setup_app
from requests import Response
from unittest.mock import patch, Mock

from .provider import SlackProvider
from custom_slack_provider.slack import CustomSlackClient, SlackException
from django.core.management import call_command


class SlackOAuth2Tests(OAuth2TestsMixin, TestCase):
    provider_id = SlackProvider.id
    provider = SlackProvider
    def setUp(self):
        call_command('loaddata', 'organisation', verbosity=0)
        setup_app(self.provider)

    def get_mocked_response(self):
        return MockedResponse(200, """{
          "ok": true,
          "url": "https:\\/\\/myteam.slack.com\\/",
          "team": {"name": "My Team", "id": "U0G9QF9C6"},
          "user": {"id": "T0G9PQBBK"},
          "team_id": "T12345",
          "user_id": "U12345"
        }""")  # noqa


class SlackClientTest(TestCase):
    def setUp(self):
        self.token = 'TEST'

    @patch('requests.get')
    def test__make_slack_get_request(self, get):
        mock_response = Mock()
        mock_response.json.return_value = {'ok': True}
        get.return_value = mock_response
        client = CustomSlackClient(self.token)
        response = client._make_slack_get_request(url='test')
        self.assertTrue(response['ok'])

        mock_response.json.return_value = {'ok': False,
                                           'error': 'Slack Error'}
        try:
            client._make_slack_get_request(url='test')
        except SlackException as e:
            self.assertTrue(isinstance(e, SlackException))
            self.assertEquals(e.message, 'Slack Error')

    @patch('requests.post')
    def test__make_slack_post_request(self, post):
        mock_response = Mock()
        mock_response.json.return_value = {'ok': True}
        post.return_value = mock_response
        client = CustomSlackClient(self.token)
        response = client._make_slack_post_request(url='test', data={})
        self.assertTrue(response['ok'])

        mock_response.json.return_value = {'ok': False,
                                           'error': 'Slack Error'}
        try:
            client._make_slack_get_request(url='test')
        except SlackException as e:
            self.assertTrue(isinstance(e, SlackException))
            self.assertEquals(e.message, 'Slack Error')

    @patch('custom_slack_provider.slack.CustomSlackClient._make_slack_get_request')
    def test_get_identity(self, _make_slack_get_request):
        _make_slack_get_request.return_value = {'user': {'id': 1}}
        client = CustomSlackClient(self.token)
        response = client.get_identity()
        self.assertEqual(response['user']['id'], 1)
