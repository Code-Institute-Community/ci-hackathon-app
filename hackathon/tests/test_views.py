from django.shortcuts import reverse
from django.test import TestCase
from accounts.models import CustomUser, Organisation
from django.utils import timezone

from hackathon.models import Hackathon


class TestHackathonViews(TestCase):
    """Tests views for the Hackathon app."""

    def setUp(self):
        """Sets up the models for testing"""
        organisation = Organisation.objects.create(display_name="CI")
        self.partner_org = Organisation.objects.create(display_name="Partner")
        self.user = CustomUser.objects.create(username="testuser", organisation=organisation)
        self.partner_user = CustomUser.objects.create(username="partnertestuser", organisation=self.partner_org)
        self.staff_user = CustomUser.objects.create(username="staffuser")
        self.staff_user.is_staff = True
        self.staff_user.save()
        self.super_user = CustomUser.objects.create(username="super_user")
        self.super_user.is_staff = True
        self.super_user.is_superuser = True
        self.super_user.save()
        self.hackathon = Hackathon.objects.create(
            created_by=self.user,
            status='published',
            display_name="hacktest",
            description="lorem ipsum",
            start_date=f'{timezone.now()}',
            end_date=f'{timezone.now()}',
            organisation=organisation)

    def test_render_hackathon_list(self):
        """Tests the correct rendering of the hackathon list page,
        including contexts."""
        self.client.force_login(self.user)
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
        self.client.force_login(self.super_user)

        hackathon = Hackathon.objects.get(pk=1)
        status_before = hackathon.status
        response = self.client.post('/hackathon/1/update_hackathon_status/',
                                    {'status': 'finished'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        hackathon = Hackathon.objects.get(pk=1)
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(status_before, hackathon.status)

    def test_view_hackathon(self):
        """Tests the correct rendering of the hackathon detail page,
        including contexts."""

        response = self.client.get('/hackathon/1/')
        # Confirms the correct template, context items
        self.assertEqual(response.status_code, 302)

        # Confirms the "enroll.html" template shows only for staff.
        self.user.is_staff = True
        self.user.save()
        self.client.force_login(self.user)

        response = self.client.get('/hackathon/1/')
        self.assertTemplateUsed(response,
                                'hackathon/hackathon_view.html')

    def test_judge_enroll_toggle(self):
        """Tests that judges can correctly enroll and withdraw"""

        self.client.force_login(self.user)

        response = self.client.post('/hackathon/enroll/',
                                    {'hackathon-id': 1},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        hackathon = Hackathon.objects.get(pk=1)

        # Confirms a non-staff user is refused
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user in hackathon.participants.all())
        self.assertFalse(self.user in hackathon.judges.all())

        # confirms staff can be enrolled as a judge
        self.staff_user.is_staff = True
        self.staff_user.save()
        self.client.force_login(self.staff_user)

        response = self.client.post('/hackathon/enroll/',
                                    {'hackathon-id': self.hackathon.id,
                                     'enrollment-type': 'judge'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.staff_user in hackathon.judges.all())

        # Confirms staff can withdraw
        response = self.client.post('/hackathon/enroll/',
                                    {'hackathon-id': self.hackathon.id,
                                     'enrollment-type': 'judge'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.staff_user in hackathon.judges.all())

    def test_has_access_to_right_hackathons(self):
        hackathon = Hackathon.objects.create(
            created_by=self.user,
            status='published',
            display_name="hacktest",
            description="lorem ipsum",
            start_date=f'{timezone.now()}',
            end_date=f'{timezone.now()}',
            organisation=self.partner_org,
            is_public=False)
        
        self.client.force_login(self.user)
        response = self.client.get(reverse('hackathon:view_hackathon', kwargs={'hackathon_id': hackathon.id}))
        self.assertEquals(response.status_code, 302)
        
        self.client.force_login(self.partner_user)
        response = self.client.get(reverse('hackathon:view_hackathon', kwargs={'hackathon_id': hackathon.id}))
        self.assertEquals(response.status_code, 200)

        self.client.force_login(self.staff_user)
        response = self.client.get(reverse('hackathon:view_hackathon', kwargs={'hackathon_id': hackathon.id}))
        self.assertEquals(response.status_code, 200)

        self.client.force_login(self.super_user)
        response = self.client.get(reverse('hackathon:view_hackathon', kwargs={'hackathon_id': hackathon.id}))
        self.assertEquals(response.status_code, 200)

        hackathon.is_public = True
        hackathon.save()

        self.client.force_login(self.user)
        response = self.client.get(reverse('hackathon:view_hackathon', kwargs={'hackathon_id': hackathon.id}))
        self.assertEquals(response.status_code, 200)

        hackathon.is_public = False
        hackathon.save()
        self.user.organisation = self.partner_org
        self.user.save()

        self.client.force_login(self.user)
        response = self.client.get(reverse('hackathon:view_hackathon', kwargs={'hackathon_id': hackathon.id}))
        self.assertEquals(response.status_code, 200)
    
    def test_partner_enroll(self):
        hackathon = Hackathon.objects.create(
            created_by=self.user,
            status='published',
            display_name="hacktest",
            description="lorem ipsum",
            start_date=f'{timezone.now()}',
            end_date=f'{timezone.now()}',
            organisation=self.partner_org,
            is_public=False)
        
        self.client.force_login(self.user)
        self.client.post('/hackathon/enroll/',
                         {'hackathon-id': hackathon.id},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue(self.user not in hackathon.participants.all())

        self.client.force_login(self.staff_user)
        self.client.post('/hackathon/enroll/',
                         {'hackathon-id': hackathon.id, 'enrollment-type': 'judge'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue(self.staff_user in hackathon.judges.all())

        self.client.force_login(self.super_user)
        self.client.post('/hackathon/enroll/',
                         {'hackathon-id': hackathon.id, 'enrollment-type': 'judge'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue(self.super_user in hackathon.judges.all())

        hackathon.is_public = True
        hackathon.save()

        self.client.force_login(self.user)
        self.client.post('/hackathon/enroll/',
                         {'hackathon-id': hackathon.id},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue(self.user in hackathon.participants.all())

        hackathon.is_public = False
        hackathon.save()
        self.user.organisation = self.partner_org
        self.user.save()

        # Check if it can also be removed
        self.client.force_login(self.user)
        self.client.post('/hackathon/enroll/',
                         {'hackathon-id': hackathon.id},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue(self.super_user not in hackathon.participants.all())

    def test_list_partner_hackathons(self):
        hackathon = Hackathon.objects.create(
            created_by=self.user,
            status='published',
            display_name="hacktest",
            description="lorem ipsum",
            start_date=f'{timezone.now()}',
            end_date=f'{timezone.now()}',
            organisation=self.partner_org,
            is_public=False)

        # if this is more than 5, the response results will have to be paginated
        # because they are capped at 5
        num_hackathons = Hackathon.objects.count()

        self.client.force_login(self.user)
        self.assertTrue(num_hackathons <= 5)
        response = self.client.get(reverse('hackathon:hackathon-list'))
        hackathons = [hackathon.id for hackathon in response.context['hackathons']]
        self.assertTrue(hackathon.id not in hackathons)

        self.client.force_login(self.staff_user)
        response = self.client.get(reverse('hackathon:hackathon-list'))
        hackathons = [hackathon.id for hackathon in response.context['hackathons']]
        self.assertTrue(hackathon.id in hackathons)

        self.client.force_login(self.super_user)
        response = self.client.get(reverse('hackathon:hackathon-list'))
        hackathons = [hackathon.id for hackathon in response.context['hackathons']]
        self.assertTrue(hackathon.id in hackathons)

        hackathon.is_public = True
        hackathon.save()
        
        self.client.force_login(self.user)
        response = self.client.get(reverse('hackathon:hackathon-list'))
        hackathons = [hackathon.id for hackathon in response.context['hackathons']]
        self.assertTrue(hackathon.id in hackathons)

        hackathon.is_public = False
        hackathon.save()
        self.user.organisation = self.partner_org
        self.user.save()

        self.client.force_login(self.user)
        response = self.client.get(reverse('hackathon:hackathon-list'))
        hackathons = [hackathon.id for hackathon in response.context['hackathons']]
        self.assertTrue(hackathon.id in hackathons)
