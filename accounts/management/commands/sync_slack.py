from django.core.management.base import BaseCommand

from accounts.helpers import sync_slack_users


class Command(BaseCommand):
    help = 'Syncs all or specified users with the information on Slack'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--users', nargs='+',
                            help='Set users to be synced',)
        parser.add_argument('-k', '--keys', nargs='+',
                            help='Set keys to be updated',)
        parser.add_argument('-i', '--interval', type=float,
                            help='Set the sleep interval in between requests',)

    def handle(self, *args, **kwargs):
        users = kwargs.get('users')
        keys = kwargs.get('keys')
        interval = kwargs.get('interval', 0.0) or 0.0

        sync_slack_users(users, keys, interval)
