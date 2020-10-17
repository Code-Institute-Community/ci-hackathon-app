from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from hackathon.models import Hackathon


class TestHackathonViews(TestCase):
    """Tests views for the Hackathon app."""

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

    def test_render_hackathon_list(self):
        """Tests the correct rendering of the hackathon list page,
        including contexts."""

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
