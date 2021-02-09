import requests

from accounts.models import CustomUser

from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import SlackProvider


class SlackOAuth2Adapter(OAuth2Adapter):
    provider_id = SlackProvider.id

    access_token_url = 'https://slack.com/api/oauth.access'
    authorize_url = 'https://slack.com/oauth/authorize'
    identity_url = 'https://slack.com/api/users.identity'
    user_detail_url = 'https://slack.com/api/users.info'

    def complete_login(self, request, app, token, **kwargs):
        extra_data = self.get_data(token.token)
        return self.get_provider().sociallogin_from_response(request,
                                                             extra_data)

    def get_data(self, token):
        # Verify the user first

        resp = requests.get(
            self.identity_url,
            params={'token': token}
        )
        resp = resp.json()

        if not resp.get('ok'):
            raise OAuth2Error()

        userid = resp.get('user', {}).get('id')
        user_info = requests.get(
            self.user_detail_url,
            params={'token': token, 'user': userid}
        )
        user_info = user_info.json()

        if not user_info.get('ok'):
            raise OAuth2Error()

        user_info = user_info.get('user', {})
        display_name = user_info.get('profile',
                                     {}).get('display_name_normalized')

        resp['user']['display_name'] = display_name
        resp['user']['username'] = user_info.get('id')
        resp['user']['full_name'] = user_info.get('profile',
                                                  {}).get('real_name')
        resp['user']['first_name'] = user_info.get('profile',
                                                  {}).get('first_name')
        resp['user']['last_name'] = user_info.get('profile',
                                                  {}).get('last_name')
        # This key is not present in the response if the user has not
        # uploaded an image and the field cannot be None
        resp['user']['image_original'] = (user_info.get(
            'profile', {}).get('image_original') or '')
        resp['user']['title'] = user_info.get('profile',
                                                  {}).get('title')
        return resp


oauth2_login = OAuth2LoginView.adapter_view(SlackOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(SlackOAuth2Adapter)
