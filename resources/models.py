from django.db import models


class Resource(models.Model):
    """Model representing a Resource that contains the resource's name, description
    and an external link to the resource. All the fields are required."""
    name = models.CharField(max_length=50)
    link = models.URLField(max_length=200)
    description = models.TextField(max_length=400, default="")

    def __str__(self):
        return self.name
