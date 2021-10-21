from django.test import TestCase
from django.utils import timezone

from accounts.models import CustomUser, Organisation
from hackathon.models import (Hackathon,
                              HackTeam,
                              HackAward,
                              HackAwardCategory,
                              HackProject,
                              HackProjectScore,
                              HackProjectScoreCategory)


class HackathonUnitTestCase(TestCase):
    def setUp(self):
        self.organisation = Organisation.objects.create()
        self.user = CustomUser.objects.create(
            username="testuser",
            slack_display_name="testuser")
        self.hackathon = Hackathon.objects.create(
            created_by=self.user,
            display_name="hacktest",
            description="lorem ipsum",
            start_date=f'{timezone.now()}',
            end_date=f'{timezone.now()}')
        self.hackathon.judges.set([self.user])

        self.project = HackProject.objects.create(
            created_by=self.user,
            display_name="testproject",
            description="lorem ipsum",
            github_url="https://www.test.com/",
            deployed_url="https://www.test.com/")

        self.team = HackTeam.objects.create(
            created_by=self.user,
            project=self.project,
            display_name="testteam",
            hackathon=self.hackathon)
        self.team.participants.set([self.user])

        self.score_category = HackProjectScoreCategory.objects.create(
            created_by=self.user,
            category="knowledge",
            min_score=1,
            max_score=15,
            is_active=True)

        self.score_category2 = HackProjectScoreCategory.objects.create(
            created_by=self.user,
            category="deployement",
            min_score=1,
            max_score=15,
            is_active=True)

        self.score_category3 = HackProjectScoreCategory.objects.create(
            created_by=self.user,
            category="theme",
            min_score=1,
            max_score=15,
            is_active=True)

        self.project_score = HackProjectScore.objects.create(
            created_by=self.user,
            judge=self.user,
            project=self.project,
            score=1,
            hack_project_score_category=self.score_category)
