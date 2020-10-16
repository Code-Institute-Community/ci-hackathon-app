from django.db import models


class Resource(models.Model):

    name = models.CharField(max_length=254)
    link = models.URLField(max_length = 200) 

    def __str__(self):
        return self.name