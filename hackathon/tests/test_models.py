from django.test import TestCase
from django.utils import timezone
from accounts.models import CustomUser, Organisation

from hackathon.models import (Hackathon,
                              HackTeam,
                              HackAwardCategory,
                              HackProject,
                              HackProjectScore,
                              HackProjectScoreCategory)


class HackathonTests(TestCase):
    """Tests fo Hackathon models."""

    def setUp(self):
        """Sets up the models for testing"""
        user = CustomUser.objects.create(slack_display_name="testuser")
        organisation = Organisation.objects.create()

        hackathon = Hackathon.objects.create(
            created_by=user,
            display_name="hacktest",
            description="lorem ipsum",
            start_date=f'{timezone.now()}',
            end_date=f'{timezone.now()}')

        team = HackTeam.objects.create(
            created_by=user,
            display_name="testteam",
            hackathon=hackathon)
        team.participants.set([user])

        HackAwardCategory.objects.create(
            created_by=user,
            display_name="testaward",
            description="lorem ipsum",
            hackathon=hackathon)

        project = HackProject.objects.create(
            created_by=user,
            display_name="testproject",
            description="lorem ipsum",
            github_url="https://www.test.com/",
            deployed_url="https://www.test.com/")

        score_category = HackProjectScoreCategory.objects.create(
            created_by=user,
            category="testcategory",
            min_score=1,
            max_score=15)
        score_category.save()

        HackProjectScore.objects.create(
            created_by=user,
            judge=user,
            project=project,
            score=1,
            hack_project_score_category=score_category)

    def test_hackathon_str(self):
        """Tests the string method on the hackathon."""
        self.assertEqual(str(Hackathon.objects.get(pk=1)), ('hacktest'))

    def test_hackteam_str(self):
        """Tests the string method on the hackathon."""
        self.assertEqual(str(HackTeam.objects.get(pk=1)), ('testteam'))

    def test_hackawardcategory_str(self):
        """Tests the string method on the hackathon."""
        self.assertEqual(str(HackAwardCategory.objects.get(pk=1)),
                         ('testaward'))

    def test_hackproject_str(self):
        """Tests the string method on the hackathon."""
        self.assertEqual(str(HackProject.objects.get(pk=1)), ('testproject'))

    def test_hackprojectscore_str(self):
        """Tests the string method on the hackathon."""
        self.assertEqual(str(HackProjectScore.objects.get(pk=1)),
                         ("testproject, testuser"))

    def test_hackprojectscorecategory_str(self):
        """Tests the string method on the hackathon."""
        self.assertEqual(str(HackProjectScoreCategory.objects.get(pk=1)),
                         ('testcategory'))
        self.assertEqual(HackProjectScoreCategory.objects.get(pk=1).min_score,
                        1)
        self.assertEqual(HackProjectScoreCategory.objects.get(pk=1).max_score,
                        15)
