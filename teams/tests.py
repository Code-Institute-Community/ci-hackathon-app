from copy import deepcopy
import math

from django.core.management import call_command
from django.test import TestCase

from accounts.models import CustomUser
from hackathon.models import Hackathon
from .helpers import (find_all_combinations, pick_from_participants,
                      pick_teams, group_participants, choose_team_sizes,
                      find_team_combinations, combine, dupe_combinations,
                      find_combinations, choose_team_levels,
                      find_combinations_with_duplicates,
                      distribute_participants_to_teams)


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

    def test_group_participants(self):
        teamsize = 3
        num_teams = len(self.participants) / teamsize
        participants, team_progression_level = group_participants(
            self.participants, num_teams)
        a = []
        for l in participants.values():
            for p in l:
                a.append(p['level'])
        print(a)
        self.assertTrue(isinstance(participants, dict))
        self.assertTrue(isinstance(team_progression_level, int))

    def test_find_all_compinations(self):
        teamsize = 3
        team_sizes = choose_team_sizes(self.participants, teamsize)
        num_teams = len(team_sizes)
        participant_groups, team_level = group_participants(
            self.participants, num_teams)
        group_levels = list(participant_groups.keys())
        combinations = find_all_combinations(group_levels, team_sizes,
                                             team_level)
        print(combinations)
        self.assertTrue(isinstance(combinations, dict))

    def test_pick_from_participants(self):
        teamsize = 3
        team_sizes = choose_team_sizes(self.participants, teamsize)
        num_teams = len(team_sizes)
        participant_groups, team_level = group_participants(
            self.participants, num_teams)
        group_levels = list(participant_groups.keys())
        combinations = find_all_combinations(group_levels, team_sizes,
                                             team_level)
        picked_participants, participants = pick_from_participants(
            list(combinations)[1], participant_groups)
        print(picked_participants)
        print(participants)
        self.assertTrue(isinstance(picked_participants, list))
        self.assertTrue(isinstance(participants, dict))

    def test_pick_teams(self):
        teamsize = 3
        teams = pick_teams(self.participants, teamsize)
        self.assertTrue(teams)

    def test_pick_logic(self):
        combination = [1, 5, 3]
        participant_groups = {
            1: [],
            5: [],
            3: []
        }
        check_sum = sum([
            1 for l in combination
            if participant_groups[l]
        ])
        print(check_sum)

    def test_find_team_combinations(self):
        teamsize = 3
        team_sizes = choose_team_sizes(self.participants, teamsize)
        num_teams = len(team_sizes)
        participant_groups, team_level = group_participants(
            self.participants, num_teams)
        group_levels = list(participant_groups.keys())
        combinations = find_all_combinations(group_levels, team_sizes,
                                             team_level)
        team_combos = find_team_combinations(team_sizes, combinations,
                                             participant_groups)
        self.assertTrue(team_combos)

    def test_combine(self):
        team_sizes_dict = {4: 1, 3: 5}
        combinations = [(1, 6, 4), (5, 2, 4), (3, 6, 2), (1, 5, 3, 2), (1, 5, 3, 2)]
        team_sizes = [4, 3, 3, 3, 3, 3]
        hackathon_level = 62
        all_options = {
            3: {
                '164': [
                    [[1, 6, 4]],
                    [[1, 6, 4], [1, 6, 4]],
                    [[1, 6, 4], [1, 6, 4], [1, 6, 4]],
                    [[1, 6, 4], [1, 6, 4], [1, 6, 4], [1, 6, 4]],
                    [[1, 6, 4], [1, 6, 4], [1, 6, 4], [1, 6, 4], [1, 6, 4]]
                ],
                '524': [
                    [[5, 2, 4]],
                    [[5, 2, 4], [5, 2, 4]],
                    [[5, 2, 4], [5, 2, 4], [5, 2, 4]],
                    [[5, 2, 4], [5, 2, 4], [5, 2, 4], [5, 2, 4]],
                    [[5, 2, 4], [5, 2, 4], [5, 2, 4], [5, 2, 4], [5, 2, 4]]
                ],
                '362': [
                    [[3, 6, 2]],
                    [[3, 6, 2], [3, 6, 2]],
                    [[3, 6, 2], [3, 6, 2], [3, 6, 2]],
                    [[3, 6, 2], [3, 6, 2], [3, 6, 2], [3, 6, 2]],
                    [[3, 6, 2], [3, 6, 2], [3, 6, 2], [3, 6, 2], [3, 6, 2]]
                ]},
            4: {
                '1532': [
                    [[1, 5, 3, 2]]
                ]
            }
        }
        combine(all_options, combinations, len(team_sizes), team_sizes, team_sizes_dict, hackathon_level)

        end_result = [[1, 4], [1, 2, 3]]

    def test_dupe_combinations(self):
        team_sizes = [3, 3, 3, 3, 3, 4]
        combos_without_dupes = find_combinations_with_duplicates(
            self.participants, team_sizes)
        print(combos_without_dupes)
        self.assertTrue(combos_without_dupes)

    def test_get_teams(self):
        teamsize = 3
        team_sizes = sorted(choose_team_sizes(self.participants, teamsize))
        grouped_participants, hackathon_level = group_participants(self.participants, len(team_sizes))
        team_levels = sorted(choose_team_levels(len(team_sizes), hackathon_level))
        combos_without_dupes = find_combinations_with_duplicates(
            self.participants, team_sizes)
        teams, leftover_participants = distribute_participants_to_teams(
            team_sizes, team_levels, grouped_participants,
            combos_without_dupes)
        self.assertTrue(teams)
            
    def test_choose_team_levels(self):
        hackathon_level = 62
        num_teams = 6
        team_scores = choose_team_levels(num_teams, hackathon_level)
        print(team_scores)
        self.assertTrue(team_scores)