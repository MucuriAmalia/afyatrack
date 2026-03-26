from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class County(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "country")

    def __str__(self):
        return self.name


class SubCounty(models.Model):
    name = models.CharField(max_length=100)
    county = models.ForeignKey(County, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "county")

    def __str__(self):
        return self.name


class Ward(models.Model):
    name = models.CharField(max_length=100)
    subcounty = models.ForeignKey(SubCounty, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "subcounty")

    def __str__(self):
        return self.name


class CommunityUnit(models.Model):
    name = models.CharField(max_length=100)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "ward")

    def __str__(self):
        return self.name


class Village(models.Model):
    name = models.CharField(max_length=100)
    community_unit = models.ForeignKey(CommunityUnit, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "community_unit")

    def __str__(self):
        return self.name