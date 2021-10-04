import json
import logging

from smtplib import SMTPException

from django.core.mail import send_mail

from .models import PartnershipRequestEmailSiteSettings

logger = logging.getLogger(__name__)


def send_partnership_request_email(data):
    try:
        settings = PartnershipRequestEmailSiteSettings.objects.first()
        if settings:
            send_mail(
                settings.subject,
                data.get("description"),
                settings.from_email,
                json.loads(settings.to_emails),
                fail_silently=False,
            )
    except json.decoder.JSONDecodeError:
        logger.exception("Error parsing to_emails. Wrong format.")
    except SMTPException:
        logger.exception("There was an issue sending the email.")
