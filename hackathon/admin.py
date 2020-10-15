from django.contrib import admin
from .models import (Hackathon,
                     HackAwardCategory,
                     HackTeam,
                     HackProject,
                     HackProjectScore,
                     HackProjectScoreCategory)


# Register your models here.
admin.site.register(Hackathon)
admin.site.register(HackAwardCategory)
admin.site.register(HackTeam)
admin.site.register(HackProject)
admin.site.register(HackProjectScore)
admin.site.register(HackProjectScoreCategory)
