from django.db import models
from django.db.models import Q
continents = ['Asia', 'Europe', 'North America', 'Africa', 'Oceania', 'Antarctica', 'South America']

class City(models.Model):
    name = models.TextField()
    country_code: models.CharField(max_length=3)
    district = models.CharField(max_length=255)
    population = models.PositiveIntegerField()


class Country(models.Model):
    code: models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=255)
    continent = models.TextField()
    region = models.CharField(max_length=255)
    surface_area = models.FloatField()
    indepyear = models.PositiveSmallIntegerField()
    population = models.PositiveIntegerField()
    lifeexpectancy = models.FloatField()
    gnp = models.DecimalField(max_digits=10, decimal_places=2)
    gnpold = models.DecimalField(max_digits=10, decimal_places=2)
    localname = models.CharField(max_length=255)
    governmentform = models.CharField(max_length=255)
    headofstate = models.CharField(max_length=255, null=True)
    capital = models.ForeignKey(City, on_delete=models.CASCADE)
    code2 = models.CharField(max_length=2)

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(continent__in=continents), name='country_continent_check')
        ]


class CountryLanguage(models.CharField):
    country_code: models.ForeignKey(Country, on_delete=models.CASCADE, primary_key=True)
    language = models.CharField(primary_key=True)
    isofficial = models.BooleanField()
    percentage = models.FloatField()

