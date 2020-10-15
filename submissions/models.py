from django.db import models

# Create your models here.

class Submissions(models.Model):
    team_name = models.CharField(max_length=120, null=True, blank=False,on_delete=models.SET_NULL)
    speaker_name = models.CharField(max_length=300, null=True, blank=True)
    repo_url = models.URLField(max_length=1024, null=False, blank=False)
    deployed_url = models.URLField(max_length=1024, null=False, blank=False)

    
