import json
import requests
from requests.auth import AuthBase

from django.conf import settings


class AuthBearer(AuthBase):
    """ Custom requests authentication class for header """
    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers["authorization"] = "Bearer " + self.token
        return request


class SlackException(Exception):
    def __init__(self, msg):
        self.message = msg


class CustomSlackClient():
    identity_url = 'https://slack.com/api/users.identity'
    user_detail_url = 'https://slack.com/api/users.info'
    create_conversation_url = 'https://slack.com/api/conversations.create'

    def __init__(self, token):
        self.token = token

    def _make_slack_get_request(self, url, params=None):
        resp = requests.get(url, auth=AuthBearer(self.token), params=params)
        resp = resp.json()

        if not resp.get('ok'):
            raise SlackException(resp.get("error"))

        return resp

    def _make_slack_post_request(self, url, data):
        resp = requests.post(url, auth=AuthBearer(self.token), data=data)
        resp = resp.json()

        if not resp.get('ok'):
            raise SlackException(resp.get("error"))

        return resp

    def get_identity(self):
        return self._make_slack_get_request(self.identity_url)

    def get_user_info(self, userid):
        params = {"user": userid}
        response = self._make_slack_get_request(self.user_detail_url,
                                                params=params)
        return response.get('user', {})

    def create_slack_channel(self, channel_name, is_private=True):
        data = {
            "name": channel_name,
            "is_private": is_private,
            "team_id": settings.SLACK_TEAM_ID,
        }
        new_channel = self._make_slack_post_request(
            self.create_conversation_url, data=data)
        return new_channel.get('channel', {})

    @staticmethod
    def trigger_welcome_workflow(data):
        res = requests.post(settings.SLACK_WELCOME_WORKFLOW_WEBHOOK,
                            data=json.dumps(data))

        # A 200 response has an empty body
        if res.status_code == 200:
            return {'ok': True}
        return res.json()
