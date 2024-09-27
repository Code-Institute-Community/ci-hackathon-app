import logging
import re
import requests
from requests.auth import AuthBase


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
    leave_conversation_url = 'https://slack.com/api/conversations.leave'

    def __init__(self, token):
        self.token = token

    def _make_slack_get_request(self, url, params=None):
        resp = requests.get(url, auth=AuthBearer(self.token), params=params)
        if resp.status_code != 200:
            raise SlackException(resp.get("error"))

        resp = resp.json()

        if not resp.get('ok'):
            raise SlackException(resp.get("error"))

        return resp

    def _make_slack_post_request(self, url, data):
        resp = requests.post(url, auth=AuthBearer(self.token), data=data)
        if resp.status_code != 200:
            return {
                'ok': False,
                'error': resp.get("error")
            }
        return resp.json()

    def get_identity(self):
        return self._make_slack_get_request(self.identity_url)

    def leave_channel(self, channel):
        data = {
            'channel': channel
        }
        leave_channel = self._make_slack_post_request(
            self.leave_conversation_url, data=data)

        if not leave_channel.get('ok'):
            print(('An error occurred leaving a Slack Channel. '
                   f'Error code: {leave_channel.get("error")}'))

        return leave_channel

    def get_user_info(self, userid):
        params = {"user": userid}
        response = self._make_slack_get_request(self.user_detail_url,
                                                params=params)
        return response.get('user', {})

    def create_slack_channel(self, channel_name, team_id, is_private=True):
        data = {
            "team_id": team_id,
            "name": channel_name,
            "is_private": is_private,
        }
        new_channel = self._make_slack_post_request(
            self.create_conversation_url, data=data)

        if not new_channel.get('ok'):
            if new_channel.get('error') == 'name_taken':
                error_msg = (f'An error occurred creating the Private Slack Channel. '
                             f'A channel with the name "{channel_name}" already '
                             f'exists. Please change your team name and try again '
                             f'or contact an administrator')
            else:
                error_msg = (f'An error occurred creating the Private Slack Channel. '
                             f'Error code: {new_channel.get("error")}')
            return {
                'ok': False,
                'error': error_msg
            }

        logger.info(f"Successfully created {channel_name} ({new_channel.get('channel', {}).get('id')}).")
        return new_channel

    def _extract_userid_from_username(self, username):
        """ Extracts the Slack userid from a hackathon platform userid
        when Slack is enabled and the account was created with a valid userid
        schema: [SLACK_USER_ID]_[WORKSPACE_TEAM_ID]"""
        if not re.match(r'[A-Z0-9]*[_]T[A-Z0-9]*', username):
            raise SlackException('Error adding user to channel')
        return username.split('_')[0]

    def invite_users_to_slack_channel(self, users, channel):
        data = {
            "users": users,
            "channel": channel,
        }
        user_added = self._make_slack_post_request(
            self.invite_conversation_url, data=data)

        if not user_added.get('ok'):
            return {
                'ok': False,
                'error': ('An error occurred adding users to Private Slack Channel {channel}. '
                          f'Error code: {user_added.get("error")}')
            }

        return user_added

    def kick_user_from_slack_channel(self, user, channel):
        data = {
            "user": user,
            "channel": channel,
        }
        user_added = self._make_slack_post_request(
            self.invite_conversation_url, data=data)

        if not user_added.get('ok'):
            return {
                'ok': False,
                'error': (f'An error occurred kicking user {user} from Private Slack Channel {channel}. '
                          f'Error code: {user_added.get("error")}')
            }

        return user_added
