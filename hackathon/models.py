from django.db import models
from django.utils import timezone
from datetime import datetime

from accounts.models import CustomUser as User
from accounts.models import Organisation
from .lists import STATUS_TYPES_CHOICES, JUDGING_STATUS_CHOICES

# Optional fields are ony set to deal with object deletion issues.
# If this isn't a problem, they can all be changed to required fields.

# The "updated" field isn't editable in admin. Neither is "submission" field.
# A custom method to auto-fill created_by fields can be made

# When it seemed relevant, I moved the ForeignKey field to another model and
# used the one listed in the schema as the related_name. I may have been
# erroneous to do so but it can be corrected easily.
# My reasoning is explained in comments above the ForeignKey fields.


class Hackathon(models.Model):
    """Model representing a Hackathon. It is connected by a foreign key to
    User, HackAwards and HackTeam. Optional Fields: judges, organiser.
    "awards" and "teams" are related tables. They have been moved to
    HackAwardCategory and HackTeam respectively. Please see comments there."""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Each model can only be created by one user: One To Many
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name="hackathons")
    display_name = models.CharField(default="", max_length=254, blank=False)
    description = models.TextField(blank=False)
    theme = models.CharField(max_length=264, blank=False)
    start_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=False)
    # Hackathons can have numerous judges and
    # users could be the judges of more than one Hackathon: Many to Many
    judges = models.ManyToManyField(User,
                                    blank=True,
                                    related_name='hackathon_judges')
    # Hackathons can have multiple participants judges and
    # users could be participating in more than one Hackathon: Many to Many
    participants = models.ManyToManyField(User,
                                    blank=True,
                                    related_name='hackathon_participants')
    # One organiser could organise more than one Hackathon: One To Many
    organiser = models.ForeignKey(User,
                                  null=True,
                                  blank=True,
                                  on_delete=models.SET_NULL,
                                  related_name="hackathon_organiser")
    organisation = models.ForeignKey(Organisation,
                                     null=True,
                                     blank=True,
                                     on_delete=models.SET_NULL,
                                     related_name='hackathon_organisation')
    status = models.CharField(
        max_length=10,
        blank=False,
        default='draft',
        choices=STATUS_TYPES_CHOICES
    )
    judging_status = models.CharField(
        max_length=16,
        blank=False,
        default='not_yet_started',
        choices=JUDGING_STATUS_CHOICES
    )
    

    def __str__(self):
        return self.display_name


class HackAwardCategory(models.Model):
    """Model representing a HackAwardCategory. It is connected by a foreign key to
    User, Hackathon and HackProject. Optional fields: winning_project."""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Each model can only be created by one user: One To Many
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name="hackawardcategories")
    display_name = models.CharField(default="", max_length=254)
    description = models.TextField()
    # a Category will only apply to one Hackathon and
    # a Hackathon has numerous categories: One to Many.
    # If the category was going to be reused, instead, use Many to Many.
    hackathon = models.ForeignKey(Hackathon,
                                  on_delete=models.CASCADE,
                                  related_name="awards")
    # One category can have one winner: One to One
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
    User, Hackathon and HackProject. Optional fields: project."""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Each model can only be created by one user: One To Many
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name="hackteams")
    display_name = models.CharField(default="", max_length=254)
    # users could be the participants of more than one Hackathon, on different
    # teams and a team is made of a number of participants - Many to Many
    # Issue is that a user could join more than one team on the same Hackathon.
    # Could use a custom save method to prevent it.
    participants = models.ManyToManyField(User,
                                          related_name='hackteam')
    # A team participates in one Hackathon and
    # a Hackathon has numerous teams: One to Many.
    hackathon = models.ForeignKey(Hackathon,
                                  on_delete=models.CASCADE,
                                  related_name="teams")
    # One to team will have one project: One to One
    project = models.OneToOneField("HackProject",
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)

    def __str__(self):
        return self.display_name


class HackProject(models.Model):
    """Model representing a HackProject. It is connected by a foreign key to
    User and HackProjectScore. Optional Fields: mentor.
    Used URLFields for the *_link fields, a CharField with URL validation.
    "scores" has been moved to HackProjectScore. See comments there."""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hackproject",)
    display_name = models.CharField(default="", max_length=255)
    description = models.TextField(max_length=500)
    github_url = models.URLField(default="", max_length=255)
    deployed_url = models.URLField(default="", max_length=255)
    submission_time = models.DateTimeField(auto_now_add=True)
    speaker_name = models.CharField(default="", max_length=225)
    share_permission = models.BooleanField(default=True)
    # A project has one mentor, a mentor has numerous projects: One to Many.
    mentor = models.ForeignKey(User,
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL,
                               related_name="hackproject_mentor")

    def __str__(self):
        return self.display_name


class HackProjectScore(models.Model):
    """Model representing a HackProjectScore. It is connected by a foreign key to
    User, HackProject and HackProjectScoreCategory."""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Each model can only be created by one user: One To Many
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name="hackprojectscores")
    # One Judge scores several scorecategories - One to Many
    judge = models.ForeignKey(User, on_delete=models.CASCADE)
    # One score is for one project, a project has numerous scores: One to Many
    project = models.ForeignKey(HackProject,
                                on_delete=models.CASCADE,
                                related_name="scores")
    score = models.IntegerField(default=0)
    # A score applies to one category, a category has many scores: One to Many
    hack_project_score_category = models.ForeignKey("HackProjectScoreCategory",
                                                    on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.project}, {self.judge}'


class HackProjectScoreCategory(models.Model):
    """Model representing a HackProjectScoreCategory. It is connected by a
    foreign key to User and HackProjectScore."""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Each model can only be created by one user - One To Many
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name="hackprojectscorecategories")
    category = models.CharField(default="", max_length=255)
    # Score Categories can have different score range (e.g. 1-10, 1-15)
    # these fields set the scale
    min_score = models.IntegerField(default=1)
    max_score = models.IntegerField(default=10)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = "Hack project score categories"
