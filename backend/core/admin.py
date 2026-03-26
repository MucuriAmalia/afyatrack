from django.contrib import admin
from .models import (
    Country,
    County,
    SubCounty,
    Ward,
    CommunityUnit,
    Village
)


admin.site.register(Country)
admin.site.register(County)
admin.site.register(SubCounty)
admin.site.register(Ward)
admin.site.register(CommunityUnit)
admin.site.register(Village)