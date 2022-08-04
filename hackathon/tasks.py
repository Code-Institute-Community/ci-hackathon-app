import logging
import os

from celery import shared_task
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from smtplib import SMTPException

from accounts.models import EmailTemplate, SlackSiteSettings

from celery import shared_task
from django.conf import settings

from accounts.models import CustomUser as User
from hackathon.models import Hackathon
from custom_slack_provider.slack import CustomSlackClient, SlackException

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
def log_user_numbers():
    users = User.objects.count()
    logger.info(f'Number of users currently: {users}')
    return


@shared_task
def create_new_slack_channel(hackathon_id, channel_name):
    """ Create a new Slack Channel/Conversation in an existing Workspace """
    if not settings.SLACK_ENABLED:
        logger.info("Slack not enabled.")
        return

    hackathon = Hackathon.objects.get(id=hackathon_id)
    logger.info(
        (f"Creating new Slack channel {channel_name} for hackathon "
         f"{hackathon.display_name} in Slack Workspace "
         f"{settings.SLACK_WORKSPACE}({settings.SLACK_TEAM_ID})"))
    slack_client = CustomSlackClient(settings.SLACK_BOT_TOKEN)
    channel = slack_client.create_slack_channel(
        channel_name, is_private=True)

    channel_id = channel.get('id')
    logger.info(f"Channel with id {channel_id} created.")

    if not channel_id:
        logger.error("No Channel Id found.")
        return

    channel_url = f'https://{settings.SLACK_WORKSPACE}.slack.com/archives/{channel_id}'  # noqa: E501
    hackathon.channel_url = channel_url
    hackathon.save()
    logger.info(f"Hackathon {hackathon.display_name} updated successfully.")

    logger.info("Adding channel admins")
    for admin in hackathon.channel_admins.all():
        try:
            slack_client.add_user_to_slack_channel(admin.username, channel_id)
        except SlackException:
            logger.exception((f"Could not add user with id {admin.id} "
                              f"to channel {channel_id}."))
