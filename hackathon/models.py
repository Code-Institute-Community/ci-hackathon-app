from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

# Commented out fields be added when the other models are finished.

# Optional fields are ony set to deal with user deletion issues.
# If this isn't a problem, they can all be changed to required fields.

# The "updated" field isn't editable in admin. Neither is "submission" field.

# When it seemed relevant, I moved the ForeignKey field to another model and
# used the one listed in the schema as the related_name. I may have been
# erroneous to do so but it can be corrected easily.


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
    judges = models.ManyToManyField(User,
                                    blank=True,
                                    related_name='hackathon_judges')
    organiser = models.ForeignKey(User,
                                  null=True,
                                  blank=True,
                                  on_delete=models.SET_NULL,
                                  related_name="hackathon_organiser")

    def __str__(self):
        return self.display_name


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
    hackathon = models.ForeignKey("Hackathon",
                                  on_delete=models.CASCADE,
                                  related_name="awards")
    winning_project = models.OneToOneField("HackProject",
                                           null=True,
                                           blank=True,
                                           on_delete=models.SET_NULL)

    def __str__(self):
        return self.display_name

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
    # It may be necessary to alter User model?
    participants = models.ManyToManyField(User,
                                          related_name='hackteam')
    hackathon = models.ForeignKey("Hackathon",
                                  on_delete=models.CASCADE,
                                  related_name="teams")
    project = models.OneToOneField("HackProject",
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)

    def __str__(self):
        return self.display_name


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
    mentor = models.ForeignKey(User,
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL,
                               related_name="hackproject_mentor")

    def __str__(self):
        return self.display_name


class HackProjectScore(models.Model):
    """Model representing a HackProjectScore. It is connected by a foreign key to 
    User and HackProjectScoreCategory."""
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name="hackprojectscore_created_by")
    judge = models.OneToOneField(User, on_delete=models.CASCADE)
    project = models.ForeignKey("HackProject",
                                on_delete=models.CASCADE,
                                related_name="scores")
    score = models.ForeignKey("HackProjectScoreCategory",
                              on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.project}, {self.judge}'


class HackProjectScoreCategory(models.Model):
    """Model representing a HackProjectScoreCategory. It is connected by a
    foreign key to User."""
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name="hackprojectscorecategory_created_by")  # NOQA E501
    category = models.CharField(default="", max_length=255)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.category}, {self.score}'

    class Meta:
        verbose_name_plural = "Hack project score categories"
