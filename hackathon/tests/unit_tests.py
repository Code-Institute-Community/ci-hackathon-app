from django.test import TestCase
from django.utils import timezone

from hackathon.helpers import create_team_judge_category_construct,\
                              create_category_team_construct,\
                              count_judges_scores
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
            max_score=15)

        self.score_category2 = HackProjectScoreCategory.objects.create(
            created_by=self.user,
            category="deployement",
            min_score=1,
            max_score=15)

        self.score_category3 = HackProjectScoreCategory.objects.create(
            created_by=self.user,
            category="theme",
            min_score=1,
            max_score=15)

        self.project_score = HackProjectScore.objects.create(
            created_by=self.user,
            judge=self.user,
            project=self.project,
            score=1,
            hack_project_score_category=self.score_category)

    def test_create_team_judge_category_construct(self):
        expected_result = {
            'testteam': {
                'team_name': 'testteam',
                'project_name': 'testproject',
                'scores': {
                    'testuser': {
                        'knowledge': 0,
                        'deployement': 0,
                        'theme': 0,
                        'Total': 0,
                        'count_scores': False,
                    }
                },
                'total_score': 0,
            }
        }
        hackathon = Hackathon.objects.filter(display_name='hacktest').first()
        categories = HackProjectScoreCategory.objects.all()
        teams_judges_construct = create_team_judge_category_construct(
            hackathon.teams.all(),
            hackathon.judges.all(),
            categories)
        self.assertEqual(expected_result, teams_judges_construct)
    
    def test_create_category_team_construct(self):
        expected_result = {
            'knowledge': {
                'testteam': 0,
            },
            'deployement': {
                'testteam': 0,
            },
            'theme': {
                'testteam': 0,
            },
        }
        hackathon = Hackathon.objects.filter(display_name='hacktest').first()
        categories = HackProjectScoreCategory.objects.all()
        categories_teams_construct = create_category_team_construct(
            hackathon.teams.all(), categories)
        self.assertEqual(categories_teams_construct, expected_result)
    
    def test_count_judges_scores(self):
        expected_results = {
            'testuser': True,
            'testuser2': False
        }
        hackathon = Hackathon.objects.filter(display_name='hacktest').first()
        user = CustomUser.objects.create(
            username="testuser2",
            slack_display_name="testuser2")
        hackathon.judges.add(user)
        hackathon.save()
        counted_judges_scores = count_judges_scores(hackathon.judges.all(), 1)
        self.assertEqual(counted_judges_scores, expected_results)
