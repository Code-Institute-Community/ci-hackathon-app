from copy import deepcopy
import math

from django.core.management import call_command
from django.test import TestCase

from accounts.models import CustomUser
from hackathon.models import Hackathon
from .helpers import choose_team_sizes, choose_team_levels,\
                     group_participants, find_group_combinations,\
                     find_all_combinations,\
                     distribute_participants_to_teams


class TeamsTestCase(TestCase):
    def setUp(self):
        call_command('loaddata', 'organisation', verbosity=0)
        call_command('loaddata', 'accounts', verbosity=0)
        call_command('loaddata', 'resources', verbosity=0)
        call_command('loaddata', 'profiles', verbosity=0)
        call_command('loaddata', 'emailaddresses', verbosity=0)
        call_command('loaddata', 'hackathons', verbosity=0)

        hackathon_id = 3
        users = CustomUser.objects.all().exclude(username="admin")
        hackathon = Hackathon.objects.get(id=hackathon_id)
        for user in users:
            hackathon.participants.add(user)
        self.participants = hackathon.participants.all()

    def test_choose_team_sizes(self):
        """ Test calculating the amount of teams needed and exact team sizes
        given the participants and a wanted team size """
        teamsize = 3
        team_sizes = choose_team_sizes(self.participants, teamsize)
        self.assertEquals(sum(team_sizes), len(self.participants))

    def test_choose_team_levels(self):
        hackathon_level = 62
        num_teams = 6
        team_scores = choose_team_levels(num_teams, hackathon_level)
        self.assertEqual(team_scores, [11, 11, 10, 10, 10, 10])

    def test_group_participants(self):
        teamsize = 3
        num_teams = len(self.participants) / teamsize
        participants, team_progression_level = group_participants(
            self.participants, num_teams)
        a = []
        for l in participants.values():
            for p in l:
                a.append(p['level'])

        self.assertTrue(isinstance(participants, dict))
        self.assertTrue(isinstance(team_progression_level, int))
    
    def test_find_group_combinations(self):
        group_levels = [1, 1, 1, 2, 3, 4]
        team_size = 2
        team_level = 5
        combinations = find_group_combinations(group_levels, team_size,
                                               team_level)
        self.assertEqual(combinations, [(1, 4), (1, 4), (1, 4), (2, 3)])

    def test_find_all_combinations(self):
        teamsize = 3
        team_sizes = sorted(choose_team_sizes(self.participants, teamsize))
        combos_without_dupes = find_all_combinations(
            self.participants, team_sizes)
        self.assertEqual(len(combos_without_dupes), 36)

    def test_distribute_participants_to_teams(self):
        teamsize = 3
        team_sizes = sorted(choose_team_sizes(self.participants, teamsize))
        grouped_participants, hackathon_level = group_participants(self.participants, len(team_sizes))
        team_levels = sorted(choose_team_levels(len(team_sizes), hackathon_level))
        combos_without_dupes = find_all_combinations(
            self.participants, team_sizes)
        teams, leftover_participants = distribute_participants_to_teams(
            team_sizes, team_levels, grouped_participants,
            combos_without_dupes)
        self.assertTrue(teams)
