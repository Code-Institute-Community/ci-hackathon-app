import logging
import os

from celery import shared_task
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from smtplib import SMTPException

from accounts.models import EmailTemplate, SlackSiteSettings

logger = logging.getLogger(__name__)


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
