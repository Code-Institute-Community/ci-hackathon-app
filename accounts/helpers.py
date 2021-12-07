import logging
import requests
import time

from django.conf import settings

from accounts.models import CustomUser as User

USER_DETAIL_URL = 'https://slack.com/api/users.info'

DEFAULT_KEYS = {
    'profile.display_name_normalized': 'slack_display_name',
    'profile.real_name': 'full_name',
    'profile.first_name': 'first_name',
    'profile.last_name': 'last_name',
    'profile.image_original': 'profile_image',
    'profile.title': 'about',
    'tz': 'timezone',
    'email': 'email'
}

logger = logging.getLogger(__name__)


def update_value(user, field, value):
    """ Updates a User's field value if a value is given """
    if not value:
        return

    setattr(user, field, value)
    user.save()


def get_keys_and_update_user(data, keys, user):
    """ Gets the specified keys from the data and updates the User """
    if keys:
        specified_keys = {
            key: value for key, value in DEFAULT_KEYS.items()
            if value in keys}
    else:
        specified_keys = DEFAULT_KEYS

    for key, field in specified_keys.items():
        _k = key.split('.')
        value = (data.get(key) if len(_k) == 1
                 else data.get(_k[0], {}).get(_k[1]))

        update_value(user, field, value)


def sync_slack_users(users, keys, interval):
    """ Sync the profile information from Slack with the the hackathon app """
    if users:
        users = User.objects.filter(username__in=users)
    else:
        users = User.objects.all()

    for user in users:
        user_id = user.username.split('_')[0]
        user_info = requests.get(
            USER_DETAIL_URL,
            params={'token': settings.SLACK_BOT_TOKEN, 'user': user_id})
        if user_info.status_code != 200:
            logger.info(f'User {user_id} not found.')
        get_keys_and_update_user(user_info.json()['user'], keys, user)
        logger.info(f'User {user_id} updated successfully.')
        time.sleep(interval)
