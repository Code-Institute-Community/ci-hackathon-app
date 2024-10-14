import logging
import re

from celery import shared_task
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from smtplib import SMTPException

from accounts.models import CustomUser as User
from accounts.models import EmailTemplate, SlackSiteSettings

from celery import shared_task
from django.conf import settings

from custom_slack_provider.slack import CustomSlackClient
from hackathon.models import Hackathon


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

    # Use a workspace admin's User Token to create the channel
    # This is required because a bot is seen as a Slack member and
    # if a workspace is set to only allow admins to create channels
    # creating the channel with a Bot Token will give an error
    admin_client = CustomSlackClient(settings.SLACK_ADMIN_TOKEN)
    channel_response = admin_client.create_slack_channel(
        team_id=settings.SLACK_TEAM_ID,
        channel_name=channel_name,
        is_private=True,
    )

    channel = channel_response.get('channel', {}).get('id')
    channel_url = f'https://{settings.SLACK_WORKSPACE}.slack.com/archives/{channel}'
    hackathon.channel_url = channel_url
    hackathon.save()
    logger.info(f"Channel with id {channel} created.")
    
    # Add admins to channel for administration purposes
    slack_admins = (hackathon.channel_admins.all()
                    if slack_site_settings.use_hackathon_slack_admins
                    else slack_site_settings.slack_admins.all())
    admin_usernames = [admin.username for admin in slack_admins]
    pattern = re.compile(r'^U[a-zA-Z0-9]*[_]T[a-zA-Z0-9]*$')
    admin_user_ids = ','.join([username.split('_')[0]
                               for username in admin_usernames
                               if pattern.match(username)])
    admin_client.invite_users_to_slack_channel(
        users=admin_user_ids,
        channel=channel,
    )


@shared_task
def invite_user_to_hackathon_slack_channel(hackathon_id, user_id):
    slack_site_settings = SlackSiteSettings.objects.first()
    if (not (settings.SLACK_ENABLED or settings.SLACK_BOT_TOKEN or settings.SLACK_ADMIN_TOKEN
             or settings.SLACK_WORKSPACE or not slack_site_settings)):
        logger.info("This feature is not enabeled.")
        return
    
    hackathon = Hackathon.objects.get(id=hackathon_id)
    user = User.objects.get(id=user_id)
    logger.info(f"Inviting user {user_id} to hackathon {hackathon_id}'s slack channel")

    admin_client = CustomSlackClient(settings.SLACK_ADMIN_TOKEN)
    channel = hackathon.channel_url.split('/')[-1]
    pattern = re.compile(r'^U[a-zA-Z0-9]*[_]T[a-zA-Z0-9]*$')
    slack_user_id = admin_client._extract_userid_from_username(user.username) 
    admin_client.invite_users_to_slack_channel(
            users=[slack_user_id],
            channel=channel
    )
    logger.info(f"Successfully invited user {user_id} to hackathon {hackathon_id}'s slack channel")   


@shared_task
def kick_user_from_hackathon_slack_channel(hackathon_id, user_id):
    slack_site_settings = SlackSiteSettings.objects.first()
    if (not (settings.SLACK_ENABLED or settings.SLACK_BOT_TOKEN or settings.SLACK_ADMIN_TOKEN
             or settings.SLACK_WORKSPACE or not slack_site_settings)):
        logger.info("This feature is not enabeled.")
        return
        
    hackathon = Hackathon.objects.get(id=hackathon_id)
    user = User.objects.get(id=user_id)
    logger.info(f"Kicking user {user_id} to hackathon {hackathon_id}'s slack channel")
    admin_client = CustomSlackClient(settings.SLACK_ADMIN_TOKEN)
    channel = hackathon.channel_url.split('/')[-1]
    pattern = re.compile(r'^U[a-zA-Z0-9]*[_]T[a-zA-Z0-9]*$')
    slack_user_id = admin_client._extract_userid_from_username(user.username)
    kicked = admin_client.kick_user_from_slack_channel(
            user=slack_user_id,
            channel=channel
    )
    logger.info(f"Successfully kicked user {user_id} to hackathon {hackathon_id}'s slack channel")

