from django.contrib import admin

from .models import Showcase, ShowcaseSiteSettings


class ShowcaseAdmin(admin.ModelAdmin):
    readonly_fields = ('hash',)


admin.site.register(Showcase, ShowcaseAdmin)
admin.site.register(ShowcaseSiteSettings)
