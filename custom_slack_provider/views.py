import logging
import requests

from accounts.models import CustomUser
from django.core.exceptions import PermissionDenied
from requests import RequestException

from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.base import AuthAction, AuthError, AuthProcess
from allauth.socialaccount.providers.base import ProviderException
from allauth.socialaccount.adapter import get_adapter
from .helpers import (
    complete_social_login,
    render_authentication_error,
)
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
    OAuth2View,
)
from allauth.socialaccount import app_settings, signals
from allauth.socialaccount.models import SocialLogin, SocialToken
from allauth.utils import build_absolute_uri, get_request_param

from django.conf import settings

from .provider import SlackProvider

logger = logging.getLogger(__name__)


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
            raise OAuth2Error(f'UserInfo Exception: {resp.get("error")}')

        userid = resp.get('user', {}).get('id')
        user_info = requests.get(
            self.user_detail_url,
            params={'token': settings.SLACK_BOT_TOKEN, 'user': userid}
        )
        user_info = user_info.json()

        if not user_info.get('ok'):
            raise OAuth2Error(f'UserInfo Exception: {user_info.get("error")}')

        user_info = user_info.get('user', {})
        display_name = user_info.get('profile',
                                     {}).get('display_name_normalized')
        teamid = resp.get('team').get('id')
        if not resp.get('user', {}).get('email'):
            resp['user']['email'] = user_info.get('email')
        resp['user']['display_name'] = display_name
        resp['user']['username'] = f'{userid}_{teamid}'
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
        resp['user']['timezone'] = user_info.get('tz')
        return resp


class CustomOAuth2CallbackView(OAuth2View):
    def dispatch(self, request, *args, **kwargs):
        if 'error' in request.GET or 'code' not in request.GET:
            # Distinguish cancel from error
            auth_error = request.GET.get('error', None)
            if auth_error == self.adapter.login_cancelled_error:
                error = AuthError.CANCELLED
            else:
                error = AuthError.UNKNOWN
            return render_authentication_error(
                request,
                self.adapter.provider_id,
                error=error)
        app = self.adapter.get_provider().get_app(self.request)
        client = self.get_client(request, app)
        try:
            access_token = client.get_access_token(request.GET['code'])
            token = self.adapter.parse_token(access_token)
            token.app = app
            login = self.adapter.complete_login(request,
                                                app,
                                                token,
                                                response=access_token)
            login.token = token
            if self.adapter.supports_state:
                login.state = SocialLogin \
                    .verify_and_unstash_state(
                        request,
                        get_request_param(request, 'state'))
            else:
                login.state = SocialLogin.unstash_state(request)
            return complete_social_login(request, login)
        except (PermissionDenied,
                OAuth2Error,
                RequestException,
                ProviderException) as e:
            return render_authentication_error(
                request,
                self.adapter.provider_id,
                exception=e)


oauth2_login = OAuth2LoginView.adapter_view(SlackOAuth2Adapter)
oauth2_callback = CustomOAuth2CallbackView.adapter_view(SlackOAuth2Adapter)
