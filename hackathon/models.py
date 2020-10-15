from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

# Commented out fields be added when the other models are finished.


# Create your models here.
class Hackathon(models.Model):
    """Model representing a Hackathon. It is connected by a foreign key to 
    User, HackAwards and HackTeam. Optional Fields: judges, organiser."""
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name="hackathon_created_by")
    display_name = models.CharField(default="", max_length=254)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
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
    """Model representing a HackAwardCategory. It is connected by a foreign key to 
    User and HackProject."""
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


class HackTeam(models.Model):
    """Model representing a HackTeam. It is connected by a foreign key to 
    User and HackProject."""
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name="hackteam_created_by")
    display_name = models.CharField(default="", max_length=254)
    participants = models.ManyToManyField(User,
                                          related_name='hackteam')
    # winning_project = models.OneToOne("HackProject",
    #                            null=True,
    #                            blank=True,
    #                            on_delete=models.SET_NULL)


class HackProject(models.Model):
    """Model representing a HackProject. It is connected by a foreign key to 
    User and HackProjectScore. Optional Fields: mentor."""
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name="hackproject_created_by")
    display_name = models.CharField(default="", max_length=255)
    description = models.TextField()
    github_link = models.CharField(default="", max_length=255)
    collab_link = models.CharField(default="", max_length=255)
    submission_time = models.DateTimeField(auto_now_add=True)
    # scores = models.ForignKey("HackProjectScore",
    #                            null=True,
    #                            blank=True,
    #                            on_delete=models.SET_NULL)
    mentor = models.ForeignKey(User,
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL,
                               related_name="hackproject_mentor")


class HackProjectScore(models.Model):
    """Model representing a HackProjectScore. It is connected by a foreign key to 
    User and HackProjectScoreCategory."""
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name="hackprojectscore_created_by")
    judge = models.ForeignKey(User, on_delete=models.CASCADE)
    # score = models.ForignKey("HackProjectScoreCategory",
    #                            null=True,
    #                            blank=True,
    #                            on_delete=models.SET_NULL)


class HackProjectScoreCategory(models.Model):
    """Model representing a HackProject. It is connected by a foreign key to 
    User and HackProjectScore. Optional Fields: mentor."""
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name="hackprojectscore_created_by")
    category = models.IntegerField()

    class Meta:
        verbose_name_plural = "Hack project score categories"
