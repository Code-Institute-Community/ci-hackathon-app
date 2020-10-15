from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


# Create your models here.
class Hackathon(models.Model):
    """Model representing a Hackathon. It is connected by a foreign key to 
    Users, HackAwards and HackTeam."""
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name="hackathon_created_by")
    display_name = models.CharField(default="", max_length=254)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    # To be added when the other models are added.
    # awards = models.ForeignKey("HackAwardCategory",
    #                            null=True,
    #                            blank=True,
    #                            on_delete=models.SET_NULL)
    # teams = models.OneToOne("HackTeam",
    #                            null=True,
    #                            blank=True,
    #                            on_delete=models.SET_NULL)
    judges = models.ManyToManyField(User,
                                    blank=True,
                                    related_name='hackathon_judges')
    organiser = models.ForeignKey(User,
                                  null=True,
                                  blank=True,
                                  on_delete=models.SET_NULL,
                                  related_name="hackathon_organiser")


class HackAwardCategory(models.Model):
    """Model representing a Hackathon. It is connected by a foreign key to 
    Users and HackProject."""
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name="hackawardcategory_created_by")
    display_name = models.CharField(default="", max_length=254)
    description = models.TextField()
    # winning_project = models.OneToOne("HackProject",
    #                            null=True,
    #                            blank=True,
    #                            on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = "Hack award categories"

