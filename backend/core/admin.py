from django.contrib import admin
from .models import (
    Country,
    County,
    SubCounty,
    Ward,
    CommunityUnit,
    Village,
    Household,
    Patient,
)


admin.site.register(Country)
admin.site.register(County)
admin.site.register(SubCounty)
admin.site.register(Ward)
admin.site.register(CommunityUnit)
admin.site.register(Village)
admin.site.register(Household)
admin.site.register(Patient)