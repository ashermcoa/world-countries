from django.db import models
from django.db.models import Q

continents = ['Asia', 'Europe', 'North America', 'Africa', 'Oceania', 'Antarctica', 'South America']


class City(models.Model):
    name = models.TextField()
    countrycode = models.CharField(max_length=3)
    district = models.TextField()
    population = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Cities'
        db_table = 'city'

    def __str__(self):
        return self.name


class Country(models.Model):
    code = models.CharField(primary_key=True, max_length=3)
    name = models.TextField()
    continent = models.TextField()
    region = models.TextField()
    surfacearea = models.FloatField()
    indepyear = models.SmallIntegerField(blank=True, null=True)
    population = models.IntegerField()
    lifeexpectancy = models.FloatField(blank=True, null=True)
    gnp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gnpold = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    localname = models.TextField()
    governmentform = models.TextField()
    headofstate = models.TextField(blank=True, null=True)
    capital = models.ForeignKey(City, models.CASCADE,
                                related_name="Capital",
                                db_column='capital',
                                blank=True,
                                null=True)
    code2 = models.CharField(max_length=2)

    class Meta:
        verbose_name_plural = 'Countries'
        constraints = [
            models.CheckConstraint(check=Q(continent__in=continents), name='country_continent_check')
        ]

    def __str__(self):
        return self.name


class CountryLanguage(models.Model):
    countrycode = models.OneToOneField(Country, models.CASCADE, db_column='countrycode', primary_key=True)
    language = models.TextField()
    isofficial = models.BooleanField()
    percentage = models.FloatField()

    class Meta:
        verbose_name_plural = 'Country Languages'
        db_table = 'countrylanguage'
        unique_together = [['countrycode', 'language']]
