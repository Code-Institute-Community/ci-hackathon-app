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

import logging

logger = logging.getLogger(__name__)


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
        profile_image = data.get('profile_image')
        about = data.get('about')
        user = sociallogin.user
        user_username(user, username or '')
        user_email(user, valid_email_or_none(email) or '')
        name_parts = (full_name or '').partition(' ')
        user_field(user, 'first_name', first_name or name_parts[0])
        user_field(user, 'last_name', last_name or name_parts[2])
        user_field(user, 'full_name', full_name)
        user_field(user, 'slack_display_name', slack_display_name)
        user_field(user, 'username', username)
        user_field(user, 'profile_image', profile_image)
        user_field(user, 'about', about)
        return user

    def is_auto_signup_allowed(self, request, sociallogin):
        # If email is specified, check for duplicate and if so, no auto signup.
        auto_signup = app_settings.AUTO_SIGNUP
        if auto_signup:
            email = user_email(sociallogin.user)
            # Let's check if auto_signup is really possible...
            if email:
                if account_settings.UNIQUE_EMAIL:
                    if email_address_exists(email):
                        logger.exception((f'User with email {email} already '
                                          f'exists.'))
                        # Oops, another user already has this address.
                        # We cannot simply connect this social account
                        # to the existing user. Reason is that the
                        # email adress may not be verified, meaning,
                        # the user may be a hacker that has added your
                        # email address to their account in the hope
                        # that you fall in their trap.  We cannot
                        # check on 'email_address.verified' either,
                        # because 'email_address' is not guaranteed to
                        # be verified.
                        auto_signup = False
                        # FIXME: We redirect to signup form -- user will
                        # see email address conflict only after posting
                        # whereas we detected it here already.
            elif app_settings.EMAIL_REQUIRED:
                # Nope, email is required and we don't have it yet...
                auto_signup = False

        return auto_signup