from django.db import models

from accounts.models import CustomUser as User
from hackathon.models import HackProject


class Showcase(models.Model):
   """ Showcase to be displayed on the showcase page """
   created = models.DateTimeField(auto_now_add=True)
   updated = models.DateTimeField(auto_now=True)
   # Each model can only be created by one user: One To Many
   created_by = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name="created_showcases")

   display_name = models.CharField(default="", max_length=255)
   hack_project = models.OneToOneField(HackProject,
                                       related_name="showcase",
                                       on_delete=models.SET_NULL,
                                       null=True)
   showcase_participants = models.ManyToManyField(User,
                                                related_name="showcases")

   showcase_image = models.TextField(
      default="",
      blank=True,
      help_text=("Image displayed on the project showcase page to promote "
                  "the project. Img should ideally be 500x800px.")
   )
   is_public = models.BooleanField(default=True)

   def __str__(self):
      return self.display_name

   class Meta:
      verbose_name = "Project Showcase"
      verbose_name_plural = "Project Showcases"
   
   def get_team(self):
      try:
         return self.hack_project.hackteam
      except:
         return None

   def get_project(self):
      try:
         return self.hack_project
      except:
         return None
