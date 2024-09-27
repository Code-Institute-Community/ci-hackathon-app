import logging
import re

from celery import shared_task
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from smtplib import SMTPException

from accounts.models import EmailTemplate, SlackSiteSettings

from celery import shared_task
from django.conf import settings

from custom_slack_provider.slack import CustomSlackClient
from hackathon.models import Hackathon
#from teams.tasks import remove_admin_from_channel


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@shared_task
def send_email_from_template(user_email, user_name, hackathon_display_name, template_name):
    try:
        template = EmailTemplate.objects.get(template_name=template_name, is_active=True)
        user_name = user_name or user_email
        slack_settings = SlackSiteSettings.objects.first()
        if slack_settings and slack_settings.enable_welcome_emails:
            send_mail(
                subject=template.subject.format(hackathon=hackathon_display_name),
                message=template.plain_text_message.format(student=user_name, hackathon=hackathon_display_name),
                html_message=template.html_message.format(student=user_name, hackathon=hackathon_display_name),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False,
            )
            logger.info("Email {template_name} sucessfully sent to user {user.id}.")
    except ObjectDoesNotExist:
        logger.exception(
            (f"There is no template with the name {template_name}."
             "Please create it on the Django Admin Panel"))
    except SMTPException:
        logger.exception("There was an issue sending the email.")


@shared_task
def create_new_hackathon_slack_channel(hackathon_id, channel_name):
    """ Create a new Slack Channel/Conversation in an existing Workspace """
    slack_site_settings = SlackSiteSettings.objects.first()
    if (not (settings.SLACK_ENABLED or settings.SLACK_BOT_TOKEN or settings.SLACK_ADMIN_TOKEN
             or settings.SLACK_WORKSPACE or not slack_site_settings)):
        logger.info("This feature is not enabeled.")
        return

    hackathon = Hackathon.objects.get(id=hackathon_id)
    logger.info(
        (f"Creating new Slack channel {channel_name} for hackathon "
         f"{hackathon.display_name} in Slack Workspace "
         f"{settings.SLACK_WORKSPACE}({settings.SLACK_TEAM_ID})"))

    admin_client = CustomSlackClient(settings.SLACK_ADMIN_TOKEN)
    channel_response = admin_client.create_slack_channel(
        team_id=settings.SLACK_TEAM_ID,
        channel_name=channel_name,
        is_private=True,
    )

    if not channel_response['ok']:
        logger.error(channel_response['error'])

    channel = channel_response.get('channel', {}).get('id')
    channel_url = f'https://{settings.SLACK_WORKSPACE}.slack.com/archives/{channel}'
    hackathon.channel_url = channel_url
    hackathon.save()
    logger.info(f"Channel with id {channel} created.")

    # Add admins to channel for administration purposes
    users = [admin.username for admin in slack_site_settings.slack_admins.all()]
    # First need to add Slack Bot to then add users to channel
    response = admin_client.invite_users_to_slack_channel(
        users=settings.SLACK_BOT_ID,
        channel=channel,
    )
    if not response['ok']:
        logger.error(response['error'])
        return

    bot_client = CustomSlackClient(settings.SLACK_BOT_TOKEN)
    pattern = re.compile(r'^U[a-zA-Z0-9]*[_]T[a-zA-Z0-9]*$')
    users_to_invite = ','.join([user.split('_')[0]
                                for user in users if pattern.match(user)])
    bot_client.invite_users_to_slack_channel(
        users=users_to_invite,
        channel=channel,
    )

    if not response['ok']:
        logger.error(response['error'])
        return

    if slack_site_settings.remove_admin_from_channel:
#        remove_admin_from_channel(users_to_invite, channel)
        pass


@shared_task
def invite_user_to_hackathon_slack_channel(hackathon_id, user_id):
    bot_client = CustomSlackClient(settings.SLACK_BOT_TOKEN)


@shared_task
def kick_user_to_hackathon_slack_channel(user, channel):
    pass
