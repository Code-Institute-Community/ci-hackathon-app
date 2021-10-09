from django.db import models

from accounts.models import CustomUser as User
from showcase.models import SingletonModel


class Review(models.Model):
    """ Participant Review to display on the home page """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, null=True, blank=True,
                                   on_delete=models.CASCADE,
                                   related_name="reviews")
    content = models.TextField()
    rating = models.FloatField(default=0.0, null=True, blank=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.created} - {self.content}'

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class PartnershipRequest(models.Model):
    """ A record from the Parntership Request form on the home page """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    company = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f'{self.created} - {self.company}'

    class Meta:
        verbose_name = 'PartnershipRequest'
        verbose_name_plural = 'PartnershipRequests'


class PartnershipRequestEmailSiteSettings(SingletonModel):
    """ Model to configure emails for the PartnershipRequest form """
    from_email = models.CharField(max_length=255)
    to_emails = models.TextField(
        default='[]',
        help_text=('This should be a list of emails (e.g. ["email1", ...]. '
                   'Default: []'))
    subject = models.CharField(max_length=255)

    def __str__(self):
        return "Partnership Request Email Site Settings"

    class Meta:
        verbose_name = 'Partnership Request Email Site Settings'
        verbose_name_plural = 'Partnership Request Email Site Settings'
