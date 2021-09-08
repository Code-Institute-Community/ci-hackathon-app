from django.core.management import call_command
from django.test import TestCase, tag

from accounts.models import CustomUser
from hackathon.models import Hackathon, HackTeam
from .helpers import choose_team_sizes, choose_team_levels,\
                     group_participants, find_group_combinations,\
                     find_all_combinations,\
                     distribute_participants_to_teams, get_users_from_ids,\
                     create_new_team_and_add_participants,\
                     create_teams_in_view


@tag('unit')
class TeamsHelpersTestCase(TestCase):
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
        for level in participants.values():
            for p in level:
                a.append(p['level'])

        self.assertTrue(isinstance(participants, dict))
        self.assertTrue(isinstance(team_progression_level, int))

    def test_find_group_combinations(self):
        group_levels = [1, 1, 1, 2, 3, 4]
        team_size = 2
        team_level = 5
        missing = 2
        combinations = find_group_combinations(group_levels, team_size,
                                               team_level, missing)
        self.assertEqual(combinations, [[1, 3], [1, 4], [2, 2], [2, 3], [2, 4],
                                        [1, 3], [2, 3], [3, 3], [1, 4],
                                        [2, 4]])

    def test_find_all_combinations(self):
        teamsize = 3
        team_sizes = sorted(choose_team_sizes(self.participants, teamsize))
        combos_without_dupes = find_all_combinations(
            self.participants, team_sizes)
        self.assertEqual(len(combos_without_dupes), 38)

    def test_distribute_participants_to_teams(self):
        teamsize = 3
        team_sizes = sorted(choose_team_sizes(self.participants, teamsize))
        grouped_participants, hackathon_level = group_participants(
            self.participants, len(team_sizes))
        team_levels = sorted(choose_team_levels(len(team_sizes),
                                                hackathon_level))
        combos_without_dupes = find_all_combinations(
            self.participants, team_sizes)
        teams, leftover_participants = distribute_participants_to_teams(
            team_sizes, team_levels, grouped_participants,
            combos_without_dupes)
        self.assertTrue(teams)

    def test_create_new_team_and_add_participants(self):
        created_by_user = CustomUser.objects.first()
        team_name = 'team_1'
        team_members = [
            {'userid': 13, 'name': 'Palpatine@test.com', 'level': 4},
            {'userid': 3, 'name': 'C-3PO@test.com', 'level': 5}
        ]
        hackathon = Hackathon.objects.first()

        new_hack_team = create_new_team_and_add_participants(
            created_by_user, team_name, team_members, hackathon)

        self.assertTrue(isinstance(new_hack_team, HackTeam))
        self.assertEqual(len(new_hack_team.participants.all()), 2)

    def test_get_users_from_ids(self):
        team_members = [
            {'userid': 13, 'name': 'Palpatine@test.com', 'level': 4},
            {'userid': 3, 'name': 'C-3PO@test.com', 'level': 5}
        ]
        users = get_users_from_ids(team_members)
        self.assertEqual(len(users), 2)
        self.assertTrue(all([isinstance(user, CustomUser) for user in users]))

    def test_create_teams_in_view(self):
        request_user = CustomUser.objects.first()
        hackathon = Hackathon.objects.filter(teams__isnull=True).first()
        teams = {
            'team_1': [
                {'userid': 13, 'name': 'Palpatine@test.com', 'level': 4},
                {'userid': 3, 'name': 'C-3PO@test.com', 'level': 5},
            ],
            'team_2': [
                {'userid': 20, 'name': 'Shmi.Skywalker@test.com', 'level': 3},
                {'userid': 14, 'name': 'Boba.Fett@test.com', 'level': 3},
                {'userid': 11, 'name': 'Han.Solo@test.com', 'level': 3},
            ]
        }
        create_teams_in_view(request_user=request_user,
                             teams=teams,
                             hackathon_id=hackathon.id)
        self.assertEqual(len(hackathon.teams.all()), 2)


@tag('end-to-end')
class TeamsViewsTestCase(TestCase):
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

        self.participant_user = CustomUser.objects.get(pk=2)
        self.admin_user = CustomUser.objects.get(pk=1)
        self.admin_user.is_superuser = True
        self.admin_user.save()

    def test_view_change_teams_with_participant_user(self):
        """ Test to see if non-staff can access the view to change teams """
        self.client.force_login(self.participant_user)
        response = self.client.get('/hackathon/1/change_teams/')
        self.assertEqual(302, response.status_code)

    def test_view_change_teams_with_admin_user(self):
        """ Test to see if staff can access the view to change teams """
        self.client.force_login(self.admin_user)
        response = self.client.get('/hackathon/1/change_teams/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('change_teams.html')
