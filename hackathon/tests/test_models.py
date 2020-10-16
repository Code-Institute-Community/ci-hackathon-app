from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

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
        user = User.objects.create(username="testuser")
        user.save()
        hackathon = Hackathon.objects.create(
            created_by=user,
            display_name="hacktest",
            description="lorem ipsum",
            start_date=f'{timezone.now()}',
            end_date=f'{timezone.now()}')
        hackathon.save()

        team = HackTeam.objects.create(
            created_by=user,
            display_name="testteam",
            hackathon=hackathon)
        team.save()
        team.participants.set([user])

        award_category = HackAwardCategory.objects.create(
            created_by=user,
            display_name="testaward",
            description="lorem ipsum",
            hackathon=hackathon)
        award_category.save()

        project = HackProject.objects.create(
            created_by=user,
            display_name="testproject",
            description="lorem ipsum",
            github_link="https://www.test.com/",
            collab_link="https://www.test.com/")
        project.save()

        score_category = HackProjectScoreCategory.objects.create(
            created_by=user,
            category="testcategory")
        score_category.save()

        score = HackProjectScore.objects.create(
            created_by=user,
            judge=user,
            project=project,
            score=1,
            hack_project_score_category=score_category)
        score.save()

    def test_hackathon_str(self):
        """Tests the string method on the hackathon."""
        self.assertEqual(str(Hackathon.objects.get(pk=1)), ('hacktest'))
