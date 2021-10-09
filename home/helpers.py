import json
import logging

from smtplib import SMTPException

from django.core.mail import send_mail

from .models import PartnershipRequestEmailSiteSettings

logger = logging.getLogger(__name__)


def create_email_template(data):
    """ Creates the Email Template"""
    template = ''
    template += f'Company: {data.get("company")}\n'
    template += f'Contact Name: {data.get("contact_name")}\n'
    template += f'Email: {data.get("email")}\n'
    template += f'Phone: {data.get("phone")}\n'
    template += f'Hackathon Idea:\n{data.get("description")}'
    return template


def create_html_email_template(data):
    """ Creates the HTML Email Template"""
    return f"""
    <p><strong>Company</strong>: {data.get('company')}</p>
    <p><strong>Contact Name</strong>: {data.get('contact_name')}</p>
    <p><strong>Email</strong>: {data.get('email')}</p>
    <p><strong>Phone</strong>: {data.get('phone')}</p>
    <p><strong>Hackathon Idea</strong>:<br>
    {data.get('description')}</p>
    """


def send_partnership_request_email(data):
    try:
        settings = PartnershipRequestEmailSiteSettings.objects.first()
        if settings:
            send_mail(
                subject=settings.subject,
                message=create_email_template(data),
                html_message=create_html_email_template(data),
                from_email=settings.from_email,
                recipient_list=json.loads(settings.to_emails),
                fail_silently=False,
            )
    except json.decoder.JSONDecodeError:
        logger.exception("Error parsing to_emails. Wrong format.")
    except SMTPException:
        logger.exception("There was an issue sending the email.")
