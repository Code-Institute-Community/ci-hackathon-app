import re
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
    invite_conversation_url = 'https://slack.com/api/conversations.invite'

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

    def _extract_userid_from_username(self, username):
        """ Extracts the Slack userid from a hackathon platform userid
        when Slack is enabled and the account was created with a valid userid
        schema: [SLACK_USER_ID]_[WORKSPACE_TEAM_ID]"""
        if not re.match(r'[A-Z0-9]*[_]T[A-Z0-9]*', username):
            raise SlackException('Error adding user to channel')
        return username.split('_')[0]

    def add_user_to_slack_channel(self, username, channel_id):
        data = {
            "user": self._extract_userid_from_username(username),
            "channel": channel_id,
        }
        user_added = self._make_slack_post_request(
            self.invite_conversation_url, data=data)
        return user_added
