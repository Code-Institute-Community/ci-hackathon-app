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
        mock_response.status_code = 200
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
        mock_response.status_code = 200
        post.return_value = mock_response
        client = CustomSlackClient(self.token)
        response = client._make_slack_post_request(url='test', data={})
        self.assertTrue(response['ok'])

        mock_response.json.return_value = {'ok': False,
                                           'error': 'Slack Error'}
        try:
            client._make_slack_post_request(url='test', data={})
        except SlackException as e:
            self.assertTrue(isinstance(e, SlackException))
            self.assertEquals(e.message, 'Slack Error')

    @patch('custom_slack_provider.slack.CustomSlackClient._make_slack_get_request')  # noqa: 501
    def test_get_identity(self, _make_slack_get_request):
        _make_slack_get_request.return_value = {'user': {'id': 1}, 'ok': True}
        client = CustomSlackClient(self.token)
        response = client.get_identity()
        self.assertEqual(response['user']['id'], 1)

    def test__extract_userid_from_username(self):
        valid_username = 'US123123_T123123'
        invalid_username = 'bob@bob.com'
        client = CustomSlackClient(self.token)
        userid = client._extract_userid_from_username(valid_username)
        self.assertEqual(userid, 'US123123')
        try:
            userid = client._extract_userid_from_username(invalid_username)
        except SlackException as e:
            self.assertTrue(isinstance(e, SlackException))
            self.assertEquals(e.message, 'Error adding user bob@bob.com to channel')

    @patch('custom_slack_provider.slack.CustomSlackClient._make_slack_post_request')  # noqa: 501
    def test_invite_users_to_slack_channel(self, _make_slack_post_request):
        _make_slack_post_request.return_value = {
            'ok': True,
            'channel': {'id': 'CH123123'}
        }
        client = CustomSlackClient(self.token)
        response = client.invite_users_to_slack_channel(users='UA123123_T15666',
                                                        channel='CH123123')
        self.assertEqual(response['channel']['id'], 'CH123123')
