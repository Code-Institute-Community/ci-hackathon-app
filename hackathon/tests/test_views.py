from django.test import TestCase
from accounts.models import CustomUser, Organisation
from django.utils import timezone

from hackathon.models import Hackathon


class TestHackathonViews(TestCase):
    """Tests views for the Hackathon app."""

    def setUp(self):
        """Sets up the models for testing"""
        user = CustomUser.objects.create(username="testuser")
        organisation = Organisation.objects.create()
        Hackathon.objects.create(
            created_by=user,
            status='published',
            display_name="hacktest",
            description="lorem ipsum",
            start_date=f'{timezone.now()}',
            end_date=f'{timezone.now()}',
            organisation=organisation)

    def test_render_hackathon_list(self):
        """Tests the correct rendering of the hackathon list page,
        including contexts."""
        user = CustomUser.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.get('/hackathon/')

        # Confirms the correct template, context items and queryset
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hackathon/hackathon_list.html')
        self.assertTemplateUsed(response,
                                'hackathon/includes/hackathon_card.html')
        self.assertTemplateUsed(response, 'hackathon/includes/paginator.html')
        self.assertTrue(response.context['page_obj'])
        self.assertQuerysetEqual(response.context['page_obj'],
                                 Hackathon.objects.all().order_by('-created'),
                                 transform=lambda x: x)

    def test_update_hackathon_status(self):
        """ Tests that the status changes """
        user = CustomUser.objects.get(pk=1)
        user.is_superuser = True
        user.save()

        self.client.force_login(user)

        hackathon = Hackathon.objects.get(pk=1)
        status_before = hackathon.status
        response = self.client.post('/hackathon/1/update_hackathon_status',
                                    {'status': 'finished'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        hackathon = Hackathon.objects.get(pk=1)
        self.assertNotEqual(status_before, hackathon.status)

    def test_view_hackathon(self):
        """Tests the correct rendering of the hackathon detail page,
        including contexts."""

        response = self.client.get('/hackathon/1/')
        # Confirms the correct template, context items
        self.assertEqual(response.status_code, 302)

        # Confirms the "enroll.html" template shows only for staff.
        user = CustomUser.objects.get(pk=1)
        user.is_staff = True
        user.save()
        self.client.force_login(user)

        response = self.client.get('/hackathon/1/')
        self.assertTemplateUsed(response,
                                'hackathon/hackathon_view.html')

    def test_judge_enroll_toggle(self):
        """Tests that judges can correctly enroll and withdraw"""

        user = CustomUser.objects.get(pk=1)
        self.client.force_login(user)

        response = self.client.post('/hackathon/enroll/',
                                    {'hackathon-id': 1},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        hackathon = Hackathon.objects.get(pk=1)

        # Confirms a non-staff user is refused
        self.assertEqual(response.status_code, 302)
        self.assertTrue(user in hackathon.participants.all())
        self.assertFalse(user in hackathon.judges.all())

        # confirms staff can be enrolled as a judge
        user.is_staff = True
        user.save()
        self.client.force_login(user)

        response = self.client.post('/hackathon/enroll/',
                                    {'hackathon-id': 1},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 302)
        self.assertTrue(user in hackathon.judges.all())

        # Confirms staff can withdraw
        response = self.client.post('/hackathon/enroll/',
                                    {'hackathon-id': 1},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 302)
        self.assertFalse(user in hackathon.judges.all())
