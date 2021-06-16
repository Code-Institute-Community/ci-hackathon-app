from django.db import models
from django.utils import timezone
from datetime import datetime

from accounts.models import CustomUser as User
from accounts.models import Organisation
from .lists import STATUS_TYPES_CHOICES

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
    HackAward and HackTeam respectively. Please see comments there."""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Each model can only be created by one user: One To Many
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name="hackathons")
    display_name = models.CharField(default="", max_length=254, blank=False)
    tag_line = models.CharField(default="", max_length=254, blank=False,
                                help_text=("Short description which will be "
                                           "displayed in the Hackathon List "
                                           "view."))
    description = models.TextField(blank=False,
                                   help_text=("Longer description which will "
                                              "be displayed in the Hackathon "
                                              "Detail view. Usually includes "
                                              "schedule and other details."))
    theme = models.CharField(default="", max_length=264, blank=False)
    start_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=False)
    team_size = models.IntegerField(default=3)
    # Hackathons can have numerous judges and
    # users could be the judges of more than one Hackathon: Many to Many
    judges = models.ManyToManyField(User,
                                    blank=True,
                                    related_name='judged_hackathons')
    # Hackathons can have multiple participants judges and
    # users could be participating in more than one Hackathon: Many to Many
    participants = models.ManyToManyField(User,
                                    blank=True,
                                    related_name='participated_hackathons')
    # Hackathons can have multiple score categories and score categories
    # Can belong to multiple hackahtons: Many to Many
    score_categories = models.ManyToManyField(
        'HackProjectScoreCategory',
        blank=True,
        related_name='hackathon_score_categories')
    # One organiser could organise more than one Hackathon: One To Many
    organiser = models.ForeignKey(User,
                                  null=True,
                                  blank=True,
                                  on_delete=models.SET_NULL,
                                  related_name="organised_hackathons")
    organisation = models.ForeignKey(Organisation,
                                     null=True,
                                     blank=True,
                                     on_delete=models.SET_NULL,
                                     related_name='hackathons')
    status = models.CharField(
        max_length=20,
        blank=False,
        default='draft',
        choices=STATUS_TYPES_CHOICES
    )
    hackathon_image = models.TextField(
        default="",
        blank=True,
        help_text=("Hackathon image.")
    )
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = "Hackathon"
        verbose_name_plural = "Hackathons"


class HackAwardCategory(models.Model):
    """Model representing a HackAwardCategory which represents a type of award
    that can be won at a hackathon"""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Each model can only be created by one user: One To Many
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name="hackawardcategories")
    display_name = models.CharField(default="", max_length=254)
    description = models.TextField()
    ranking = models.IntegerField(null=True)

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = "Hack Award Category"
        verbose_name_plural = "Hack Award Categories"


class HackAward(models.Model):
    """Model representing a HackAward. This is the connection between the
    Hackathon, HackAwardCategory and (winning) HackProject"""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Each model can only be created by one user: One To Many
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name="hackawards")
    # a Category will only apply to one Hackathon and
    # a Hackathon has numerous categories: One to Many.
    # If the category was going to be reused, instead, use Many to Many.
    hackathon = models.ForeignKey(Hackathon,
                                  on_delete=models.CASCADE,
                                  related_name="awards")
    hack_award_category = models.ForeignKey(HackAwardCategory,
                                            on_delete=models.CASCADE,
                                            related_name="award")
    # One category can have one winner: One to One
    winning_project = models.ForeignKey("HackProject",
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.hack_award_category}, {self.hackathon}'

    class Meta:
        unique_together = ['hackathon', 'hack_award_category']
        verbose_name = "Hack Award"
        verbose_name_plural = "Hack Awards"


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
    header_image = models.TextField(
        default="",
        blank=True,
        help_text=("Image displayed at the top of the team's page.")
    )
    # users could be the participants of more than one Hackathon, on different
    # teams and a team is made of a number of participants - Many to Many
    # Issue is that a user could join more than one team on the same Hackathon.
    # Could use a custom save method to prevent it.
    participants = models.ManyToManyField(User,
                                          related_name="hackteam")
    # A team has one mentor, a mentor has numerous teams: One to Many.
    mentor = models.ForeignKey(User,
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL,
                               related_name="mentored_teams")
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
    communication_channel = models.CharField(
        default="", max_length=255, blank=True,
        help_text=("Usually a link to the Slack group IM, but can be a link "
                   "to something else."))

    def __str__(self):
        return self.display_name
    
    class Meta:
        verbose_name = "Hack Team"
        verbose_name_plural = "Hack Teams"
        unique_together = ["display_name", "hackathon"]


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
    technologies_used = models.CharField(
        default="", max_length=1024, 
        help_text=("Add any technologies that were used for this project"))
    project_image = models.TextField(
        default="",
        blank=True,
        help_text=("Image displayed next to the project on the team's page.")
    )
    screenshot = models.TextField(
        default="",
        blank=True,
        help_text=("Project screenshot displayed on the team's page "
                   "underneath the project information")
    )
    github_url = models.URLField(default="", max_length=255)
    deployed_url = models.URLField(default="", max_length=255)
    submission_time = models.DateTimeField(auto_now_add=True)
    speaker_name = models.CharField(default="", max_length=225)
    share_permission = models.BooleanField(default=True)

    def __str__(self):
        return self.display_name
    
    def get_showcase(self):
       try:
          return self.showcase
       except:
          return None


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
