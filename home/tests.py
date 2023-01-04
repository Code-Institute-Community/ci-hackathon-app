
from django.shortcuts import reverse
from django.test import TestCase
from accounts.models import CustomUser, Organisation
from django.utils import timezone

from hackathon.models import Hackathon


class TestHackathonViews(TestCase):
    def setUp(self):
        self.organisation = Organisation.objects.create(display_name="CI")
        self.partner_org = Organisation.objects.create(display_name="Partner")
        self.user = CustomUser.objects.create(username="testuser", organisation=self.organisation)
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
            organisation=self.organisation,
            is_public=True)

    def test_list_hackathons_for_non_authenticated_user(self):
        hackathon = Hackathon.objects.create(
            created_by=self.user,
            status='finished',
            display_name="hacktest2",
            description="lorem ipsum",
            start_date=f'{timezone.now()}',
            end_date=f'{timezone.now()}',
            organisation=self.partner_org,
            is_public=False)
        
        hackathon2 = Hackathon.objects.create(
            created_by=self.user,
            status='published',
            display_name="hacktest3",
            description="lorem ipsum",
            start_date=f'{timezone.now()}',
            end_date=f'{timezone.now()}',
            organisation=self.partner_org,
            is_public=False)
        
        hackathon3 = Hackathon.objects.create(
            created_by=self.user,
            status='finished',
            display_name="hacktest2",
            description="lorem ipsum",
            start_date=f'{timezone.now()}',
            end_date=f'{timezone.now()}',
            organisation=self.organisation,
            is_public=False)

        # if this is more than 5, the response results will have to be paginated
        # because they are capped at 5
        num_hackathons = Hackathon.objects.count()
        self.assertTrue(num_hackathons <= 5)

        response = self.client.get(reverse('home'))
        recent_hackathons = [hackathon.id for hackathon in response.context['recent_hackathons']]
        upcoming_hackathons = [hackathon.id for hackathon in response.context['upcoming_hackathons']]
        self.assertEquals(len(recent_hackathons), 0)
        self.assertEquals(len(upcoming_hackathons), 1)
        self.assertTrue(hackathon.id not in recent_hackathons)
        self.assertTrue(hackathon2.id not in upcoming_hackathons)

        hackathon3.is_public = True
        hackathon3.save()

        response = self.client.get(reverse('home'))
        recent_hackathons = [hackathon.id for hackathon in response.context['recent_hackathons']]
        upcoming_hackathons = [hackathon.id for hackathon in response.context['upcoming_hackathons']]
        self.assertEquals(len(recent_hackathons), 1)
        self.assertEquals(len(upcoming_hackathons), 1)

        hackathon2.is_public = True
        hackathon2.save()

        response = self.client.get(reverse('home'))
        recent_hackathons = [hackathon.id for hackathon in response.context['recent_hackathons']]
        upcoming_hackathons = [hackathon.id for hackathon in response.context['upcoming_hackathons']]
        self.assertEquals(len(upcoming_hackathons), 2)
        self.assertEquals(len(recent_hackathons), 1)

        self.user.organisation = self.partner_org
        self.user.save()
        self.client.force_login(self.user)

        response = self.client.get(reverse('home'))
        recent_hackathons = [hackathon.id for hackathon in response.context['recent_hackathons']]
        upcoming_hackathons = [hackathon.id for hackathon in response.context['upcoming_hackathons']]
        self.assertEquals(len(upcoming_hackathons), 2)
        self.assertEquals(len(recent_hackathons), 2)

    def test_list_partner_hackathons_on_home(self):
        hackathon = Hackathon.objects.create(
            created_by=self.user,
            status='finished',
            display_name="hacktest2",
            description="lorem ipsum",
            start_date=f'{timezone.now()}',
            end_date=f'{timezone.now()}',
            organisation=self.partner_org,
            is_public=False)
        
        hackathon2 = Hackathon.objects.create(
            created_by=self.user,
            status='published',
            display_name="hacktest3",
            description="lorem ipsum",
            start_date=f'{timezone.now()}',
            end_date=f'{timezone.now()}',
            organisation=self.partner_org,
            is_public=False)

        # if this is more than 5, the response results will have to be paginated
        # because they are capped at 5
        num_hackathons = Hackathon.objects.count()
        self.assertTrue(num_hackathons <= 5)

        self.client.force_login(self.user)
        response = self.client.get(reverse('home'))
        recent_hackathons = [hackathon.id for hackathon in response.context['recent_hackathons']]
        upcoming_hackathons = [hackathon.id for hackathon in response.context['upcoming_hackathons']]
        self.assertTrue(hackathon.id not in recent_hackathons)
        self.assertTrue(hackathon2.id not in upcoming_hackathons)

        self.client.force_login(self.staff_user)
        response = self.client.get(reverse('home'))
        recent_hackathons = [hackathon.id for hackathon in response.context['recent_hackathons']]
        upcoming_hackathons = [hackathon.id for hackathon in response.context['upcoming_hackathons']]
        self.assertTrue(hackathon.id in recent_hackathons)
        self.assertTrue(hackathon2.id in upcoming_hackathons)

        self.client.force_login(self.super_user)
        response = self.client.get(reverse('home'))
        recent_hackathons = [hackathon.id for hackathon in response.context['recent_hackathons']]
        upcoming_hackathons = [hackathon.id for hackathon in response.context['upcoming_hackathons']]
        self.assertTrue(hackathon.id in recent_hackathons)
        self.assertTrue(hackathon2.id in upcoming_hackathons)

        hackathon.is_public = True
        hackathon.save()
        hackathon2.is_public = True
        hackathon2.save()
        
        self.client.force_login(self.user)
        response = self.client.get(reverse('home'))
        recent_hackathons = [hackathon.id for hackathon in response.context['recent_hackathons']]
        upcoming_hackathons = [hackathon.id for hackathon in response.context['upcoming_hackathons']]
        self.assertTrue(hackathon.id in recent_hackathons)
        self.assertTrue(hackathon2.id in upcoming_hackathons)

        hackathon.is_public = False
        hackathon.save()
        hackathon2.is_public = False
        hackathon2.save()
        self.user.organisation = self.partner_org
        self.user.save()

        self.client.force_login(self.user)
        response = self.client.get(reverse('home'))
        recent_hackathons = [hackathon.id for hackathon in response.context['recent_hackathons']]
        upcoming_hackathons = [hackathon.id for hackathon in response.context['upcoming_hackathons']]
        self.assertTrue(hackathon.id in recent_hackathons)
        self.assertTrue(hackathon2.id in upcoming_hackathons)
