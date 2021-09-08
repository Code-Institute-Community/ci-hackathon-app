from django.test import TestCase
from .models import Resource


class TestResourceModels(TestCase):
    """Tests for Resource models."""

    def setUp(self):
        """Sets up the model for testing"""
        Resource.objects.create(
            name='Forking',
            link="https://www.youtube.com/watch?v=HbSjyU2vf6Y",
            description="lorem ipsum")
        Resource.objects.create(
            name='The Git Story',
            link="https://eventyret.github.io/the-git-story/",
            description="lorem ipsum")

    def test__str_method_returns_name(self):
        """Tests the string method on a resource."""
        resource = Resource.objects.create(
            name='The Git Story',
            link="https://eventyret.github.io/the-git-story/",
            description="lorem ipsum")

        self.assertEqual(resource.__str__(), "The Git Story")
