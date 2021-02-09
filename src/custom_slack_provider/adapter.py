from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email, user_field, user_username
from allauth.utils import (
    deserialize_instance,
    email_address_exists,
    import_attribute,
    serialize_instance,
    valid_email_or_none,
)


class CustomSlackSocialAdapter(DefaultSocialAccountAdapter):
    def __init__(self, adapter):
        self = adapter

    def populate_user(self,
                      request,
                      sociallogin,
                      data):
        """
        Hook that can be used to further populate the user instance.

        For convenience, we populate several common fields.

        Note that the user instance being populated represents a
        suggested User instance that represents the social user that is
        in the process of being logged in.

        The User instance need not be completely valid and conflict
        free. For example, verifying whether or not the username
        already exists, is not a responsibility.

        Overwriting original function to pull in extra information
        """
        username = data.get('username')
        full_name = data.get('full_name')
        slack_display_name = data.get('slack_display_name')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        user = sociallogin.user
        user_username(user, username or '')
        user_email(user, valid_email_or_none(email) or '')
        name_parts = (full_name or '').partition(' ')
        user_field(user, 'first_name', first_name or name_parts[0])
        user_field(user, 'last_name', last_name or name_parts[2])
        user_field(user, 'full_name', full_name)
        user_field(user, 'slack_display_name', slack_display_name)
        user_field(user, 'username', username)
        return user
