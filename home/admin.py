from django.contrib import admin

from .models import Review, PartnershipRequest, \
                    PartnershipRequestEmailSiteSettings


admin.site.register(PartnershipRequest)
admin.site.register(PartnershipRequestEmailSiteSettings)
admin.site.register(Review)
