from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount import app_settings

from custom_slack_provider.adapter import CustomSlackSocialAdapter


class SlackAccount(ProviderAccount):
    def get_avatar_url(self):
        return self.account.extra_data.get('user').get('image_192', None)

    def to_str(self):
        dflt = super(SlackAccount, self).to_str()
        return '%s (%s)' % (
            self.account.extra_data.get('name', ''),
            dflt,
        )


class SlackProvider(OAuth2Provider):
    id = 'custom_slack_provider'
    name = 'Custom Slack Provider'
    account_class = SlackAccount

    def sociallogin_from_response(self, request, response):
        from allauth.socialaccount.adapter import get_adapter
        from allauth.socialaccount.models import SocialLogin, SocialAccount
        adapter = get_adapter(request)
        adapter = CustomSlackSocialAdapter(adapter)
        uid = self.extract_uid(response)
        extra_data = self.extract_extra_data(response)
        common_fields = self.extract_common_fields(response)
        socialaccount = SocialAccount(extra_data=extra_data,
                                      uid=uid,
                                      provider=self.id)
        email_addresses = self.extract_email_addresses(response)
        self.cleanup_email_addresses(common_fields.get('email'),
                                     email_addresses)
        sociallogin = SocialLogin(account=socialaccount,
                                  email_addresses=email_addresses)
        user = sociallogin.user = adapter.new_user(request, sociallogin)
        user.set_unusable_password()
        adapter.populate_user(request, sociallogin, common_fields)
        return sociallogin

    def extract_uid(self, data):
        return "%s_%s" % (str(data.get('team').get('id')),
                          str(data.get('user').get('id')))

    def extract_common_fields(self, data):
        user = data.get('user', {})
        return {
                'username': user.get('username'),
                'full_name': user.get('full_name'),
                'slack_display_name': user.get('display_name'),
                'email': user.get('email', None),
                'profile_image': user.get('image_original'),
                'about': user.get('title')}

    def get_default_scope(self):
        return ['identify']


provider_classes = [SlackProvider]
