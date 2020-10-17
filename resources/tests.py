from django.test import TestCase
from .models import Resource


class TestResourceModels(TestCase):

    def test_Resource_created_correctly(self):

        resource1 = Resource.objects.create(name = 'Forking', link = "https://www.youtube.com/watch?v=HbSjyU2vf6Y")
        resource2 = Resource.objects.create(name = 'The Git Story', link = "https://eventyret.github.io/the-git-story/")
        resource1.save()
        resource2.save()
        self.assertEquals(resource1.name, 'Forking')
        self.assertEquals(resource1.link, 'https://www.youtube.com/watch?v=HbSjyU2vf6Y')
        self.assertEquals(resource2.name, 'The Git Story')
        self.assertEquals(resource2.link, 'https://eventyret.github.io/the-git-story/')

    
    def test__str_method_returns_name(self):

        resource = Resource.objects.create(name = 'The Git Story',link = "https://eventyret.github.io/the-git-story/")

        self.assertEqual(resource.__str__(), "The Git Story")